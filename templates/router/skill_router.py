from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional, Set, Tuple
import re


@dataclass
class SkillMatch:
    skill_name: str
    score: float
    reason: str


class SkillRouter:
    """Intent router that supports explicit slash commands and natural-language routing."""

    def __init__(self, available_skills: Optional[Set[str]] = None) -> None:
        self.available_skills = available_skills or set()
        self.skill_keywords: Dict[str, Dict[str, List[str]]] = {
            "decision_radar": {
                "high": [
                    "signal", "signals", "industry signal", "what changed", "latest shift",
                    "recent change", "industry move", "platform move", "new development",
                    "news", "recently", "过去几天", "最近发生", "行业变化", "信号", "变化",
                ],
                "medium": [
                    "ai industry", "media", "technology", "platform", "announcement",
                    "发布", "上线", "动态", "趋势信号",
                ],
            },
            "trend_distiller": {
                "high": [
                    "trend", "macro trend", "where is this going", "future of", "next stage",
                    "what happens next", "long term", "structural change",
                    "趋势", "大趋势", "未来会怎样", "接下来会怎样", "长期", "结构性变化",
                ],
                "medium": [
                    "collapse", "shift", "evolution", "saturation", "oversupply", "declining",
                    "衰落", "转向", "演化", "饱和", "过剩",
                ],
            },
            "opportunity_scanner": {
                "high": [
                    "opportunity", "opportunities", "where is the opportunity",
                    "what can be built", "what should i build", "startup opportunity",
                    "机会", "有什么机会", "哪里有机会", "可以做什么", "该做什么",
                ],
                "medium": ["gap", "white space", "window", "timing", "why now", "空白", "窗口", "时机"],
            },
            "idea_forge": {
                "high": [
                    "idea", "product idea", "generate an idea", "new app", "new product",
                    "mvp", "prototype", "build something", "我想做一个", "产品点子",
                    "新产品", "新应用", "原型", "做个东西",
                ],
                "medium": ["experiment", "feature", "tool", "agent", "workflow", "实验", "功能", "工具", "代理", "工作流"],
            },
            "product_killer": {
                "high": [
                    "will this work", "would this work", "is this viable", "good idea or not",
                    "fatal risk", "why it may fail", "should i build this", "kill or proceed",
                    "这个能行吗", "可行吗", "会不会失败", "值不值得做", "该不该做",
                    "风险", "致命问题", "会死吗",
                ],
                "medium": ["competition", "distribution", "regulation", "moat", "retention", "竞争", "分发", "监管", "壁垒", "留存"],
            },
            "founder_mode": {
                "high": [
                    "decision", "should we", "should i", "founder", "team", "strategy",
                    "hire", "fire", "focus", "priority", "resource allocation",
                    "决策", "我该不该", "团队", "战略", "优先级", "资源分配", "聚焦",
                ],
                "medium": ["execution", "founder problem", "tradeoff", "organizational", "执行", "取舍", "组织"],
            },
            "personal_os": {
                "high": [
                    "i feel", "my state", "my energy", "i am tired", "i am excited",
                    "today focus", "what should i focus on", "mental state",
                    "我现在", "我的状态", "今天该聚焦什么", "我很累", "我很兴奋", "今天重点",
                ],
                "medium": ["emotion", "burnout", "scattered", "discipline", "momentum", "情绪", "疲惫", "分散", "自律", "节奏"],
            },
            "taste_curator": {
                "high": [
                    "what should i listen to", "music recommendation", "albums for today",
                    "recommend music", "playlist", "今日听什么", "推荐音乐", "推荐专辑", "歌单", "听什么",
                ],
                "medium": ["alternative", "rock", "folk", "gospel", "ambient", "experimental", "摇滚", "民谣", "福音", "氛围", "实验音乐"],
            },
            "second_brain": {
                "high": [
                    "i'm thinking about", "help me think", "how should i understand",
                    "what does this mean", "let's think", "explore this",
                    "我在想", "帮我想想", "怎么理解", "这意味着什么", "我们来想想",
                ],
                "medium": ["contradiction", "frame", "hypothesis", "model", "paradox", "矛盾", "框架", "假设", "模型", "悖论"],
            },
        }
        self.command_aliases: Dict[str, str] = {
            "/radar": "decision_radar",
            "/trend": "trend_distiller",
            "/opportunity": "opportunity_scanner",
            "/forge": "idea_forge",
            "/kill": "product_killer",
            "/founder": "founder_mode",
            "/os": "personal_os",
            "/taste": "taste_curator",
            "/think": "second_brain",
        }

    def route(self, message: str) -> SkillMatch:
        text = self._normalize(message)

        command_match = self._match_command(text)
        if command_match:
            return self._ensure_available(command_match)

        scored_matches = self._score_all_skills(text)
        if not scored_matches:
            return SkillMatch(
                skill_name="second_brain",
                score=0.0,
                reason="No strong keyword match found; fallback to second_brain.",
            )

        best = max(scored_matches, key=lambda x: x.score)
        best = self._apply_priority_rules(text, best, scored_matches)
        if best.score < 1.0:
            best = SkillMatch(
                skill_name="second_brain",
                score=best.score,
                reason=f"Low confidence ({best.score:.2f}); fallback to second_brain.",
            )
        return self._ensure_available(best)

    def _match_command(self, text: str) -> Optional[SkillMatch]:
        for cmd, skill in self.command_aliases.items():
            if text.startswith(cmd):
                return SkillMatch(skill_name=skill, score=999.0, reason=f"Explicit command match: {cmd}")
        return None

    def _score_all_skills(self, text: str) -> List[SkillMatch]:
        matches: List[SkillMatch] = []
        for skill_name, weights in self.skill_keywords.items():
            score = 0.0
            reasons: List[str] = []
            for kw in weights.get("high", []):
                if self._contains(text, kw):
                    score += 2.5
                    reasons.append(f'high:"{kw}"')
            for kw in weights.get("medium", []):
                if self._contains(text, kw):
                    score += 1.0
                    reasons.append(f'medium:"{kw}"')
            score_boost, extra_reason = self._shape_heuristics(skill_name, text)
            score += score_boost
            if extra_reason:
                reasons.append(extra_reason)
            if score > 0:
                matches.append(SkillMatch(skill_name=skill_name, score=score, reason=", ".join(reasons)))
        return matches

    def _shape_heuristics(self, skill_name: str, text: str) -> Tuple[float, Optional[str]]:
        question_patterns = [
            r"should i\b",
            r"should we\b",
            r"can this work\b",
            r"will this work\b",
            r"would this work\b",
            r"would .* work\b",
            r"我该不该",
            r"能不能",
            r"可不可以",
            r"值不值得",
        ]
        if skill_name == "product_killer" and any(re.search(p, text) for p in question_patterns):
            return 1.5, "heuristic: viability/evaluation question"
        if skill_name == "idea_forge" and ("build" in text or "做一个" in text or "想做" in text):
            return 1.5, "heuristic: build/product creation intent"
        if skill_name == "second_brain" and (len(text.split()) > 18 or len(text) > 40):
            return 0.8, "heuristic: long reflective message"
        if skill_name == "trend_distiller" and ("future of" in text or "未来" in text or "接下来" in text):
            return 1.2, "heuristic: future-facing trend question"
        if skill_name == "personal_os" and ("我现在" in text or "today" in text or "今天" in text):
            return 0.8, "heuristic: current-state reflection"
        return 0.0, None

    def _apply_priority_rules(self, text: str, best: SkillMatch, matches: List[SkillMatch]) -> SkillMatch:
        top_map = {m.skill_name: m for m in matches}
        if ("opportunity" in text or "机会" in text) and "opportunity_scanner" in top_map:
            return top_map["opportunity_scanner"]
        if ("should i build" in text or "该不该做" in text or "值不值得做" in text) and "product_killer" in top_map:
            return top_map["product_killer"]
        if ("我的状态" in text or "我现在" in text or "today focus" in text or "今天重点" in text) and "personal_os" in top_map:
            return top_map["personal_os"]
        if ("listen to" in text or "推荐音乐" in text or "歌单" in text or "playlist" in text) and "taste_curator" in top_map:
            return top_map["taste_curator"]
        return best

    def _ensure_available(self, match: SkillMatch) -> SkillMatch:
        if not self.available_skills:
            return match
        if match.skill_name in self.available_skills:
            return match
        if "second_brain" in self.available_skills:
            return SkillMatch(
                skill_name="second_brain",
                score=match.score,
                reason=f"{match.reason}; mapped skill not installed, fallback to second_brain.",
            )
        return match

    @staticmethod
    def _normalize(text: str) -> str:
        return re.sub(r"\s+", " ", text.strip().lower())

    @staticmethod
    def _contains(text: str, keyword: str) -> bool:
        return keyword.lower() in text
