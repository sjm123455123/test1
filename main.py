import os
from typing import List, Dict, Any
from dataclasses import dataclass
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import HumanMessage, SystemMessage

# ================= 配置区域 =================
# 请在此处填入你的智谱 AI API Key
# 获取地址：https://open.bigmodel.cn/
ZHIPU_API_KEY = "your_zhipu_api_key_here"

# 初始化智谱 AI GLM-4 模型
llm = ChatOpenAI(
    temperature=0.7,
    model="glm-4",
    openai_api_key=ZHIPU_API_KEY,
    openai_api_base="https://open.bigmodel.cn/api/paas/v4/"
)
# ===========================================

# --- 基础数据结构 ---
@dataclass
class Paper:
    title: str
    authors: str
    abstract: str
    year: int

@dataclass
class ReviewSection:
    topic: str
    content: str
    references: List[str]

# --- 基础 Agent 类 ---
class BaseAgent:
    def __init__(self, name: str):
        self.name = name

# --- 具体 Agent 实现 ---

class LiteratureSearchAgent(BaseAgent):
    """模拟文献检索Agent (演示用，实际可接入IEEE/arXiv API)"""
    def run(self, query: str) -> List[Paper]:
        print(f"[{self.name}] 正在检索关于 '{query}' 的文献...")
        return [
            Paper(
                title="Deep Learning for Natural Language Processing: A Survey",
                authors="Zhang, Y., et al.",
                abstract="This paper surveys recent advances in deep learning for NLP, covering CNNs, RNNs, and Transformers. It discusses applications in machine translation, sentiment analysis, and question answering.",
                year=2023
            ),
            Paper(
                title="Attention Is All You Need",
                authors="Vaswani, A., et al.",
                abstract="We propose the Transformer, a new network architecture based solely on attention mechanisms, dispensing with recurrence and convolutions entirely. Experiments show superiority in machine translation.",
                year=2017
            ),
            Paper(
                title="BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding",
                authors="Devlin, J., et al.",
                abstract="We introduce BERT, a bidirectional transformer pre-trained on a large corpus. It achieves state-of-the-art results on a wide range of NLP tasks including GLUE and SQuAD.",
                year=2019
            )
        ]

class LiteratureAnalysisAgent(BaseAgent):
    """文献精读Agent (调用GLM-4)"""
    def run(self, papers: List[Paper]) -> str:
        print(f"[{self.name}] 正在调用 AI 分析文献核心观点...")
        
        papers_text = "\n\n".join([
            f"Title: {p.title}\nAuthors: {p.authors}\nYear: {p.year}\nAbstract: {p.abstract}"
            for p in papers
        ])
        
        prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content="你是一个专业的学术助手。请仔细阅读以下文献列表，提取每篇文献的核心贡献、方法论和创新点。"),
            HumanMessage(content=f"请分析以下文献：\n\n{papers_text}")
        ])
        
        response = llm.invoke(prompt.format_messages())
        return response.content

class LogicSynthesisAgent(BaseAgent):
    """逻辑梳理Agent (调用GLM-4进行长链推理)"""
    def run(self, analysis_content: str) -> List[ReviewSection]:
        print(f"[{self.name}] 正在梳理研究脉络并生成综述...")
        
        prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content="你是一个擅长写文献综述的教授。请根据以下文献分析内容，撰写一篇结构化的文献综述。\n要求：\n1. 分为2-3个逻辑章节\n2. 每个章节必须包含具体的文献引用\n3. 输出格式为：章节标题|||综述内容|||参考文献(分号分隔)"),
            HumanMessage(content=f"文献分析内容：\n\n{analysis_content}")
        ])
        
        response = llm.invoke(prompt.format_messages())
        
        # 解析返回结果
        sections = []
        lines = response.content.strip().split('\n')
        for line in lines:
            if '|||' in line:
                parts = line.split('|||')
                if len(parts) >= 3:
                    sections.append(ReviewSection(
                        topic=parts[0].strip(),
                        content=parts[1].strip(),
                        references=[r.strip() for r in parts[2].split(';')]
                    ))
        
        return sections if sections else [ReviewSection("1. 研究概述", response.content, ["综合文献分析"])]

class FormattingAgent(BaseAgent):
    """格式规范Agent"""
    def run(self, sections: List[ReviewSection]) -> str:
        print(f"[{self.name}] 正在生成最终 Markdown 文档...")
        
        md_content = "# 文献综述：基于大模型的自然语言处理进展\n\n"
        md_content += "## 1. 引言\n\n本文综述了自然语言处理领域的最新进展，重点关注 Transformer 架构及其后续影响。\n\n"
        
        for section in sections:
            md_content += f"## {section.topic}\n\n"
            md_content += f"{section.content}\n\n"
            md_content += "### 参考文献\n"
            for ref in section.references:
                md_content += f"- {ref}\n"
            md_content += "\n"
        
        return md_content

# --- 多 Agent 协调器 ---
class MultiAgentOrchestrator:
    def __init__(self):
        self.search_agent = LiteratureSearchAgent()
        self.analysis_agent = LiteratureAnalysisAgent()
        self.synthesis_agent = LogicSynthesisAgent()
        self.formatting_agent = FormattingAgent()

    def generate_review(self, topic: str) -> str:
        print(f"[System] 启动文献综述生成流程，主题: {topic}\n")
        
        papers = self.search_agent.run(topic)
        analysis = self.analysis_agent.run(papers)
        sections = self.synthesis_agent.run(analysis)
        final_review = self.formatting_agent.run(sections)
        
        print("\n[System] 生成完成！")
        return final_review

# --- 运行入口 ---
if __name__ == "__main__":
    if ZHIPU_API_KEY == "your_zhipu_api_key_here":
        print("⚠️  请先在代码中填入你的智谱 AI API Key！")
        print("获取地址：https://open.bigmodel.cn/")
    else:
        orchestrator = MultiAgentOrchestrator()
        review = orchestrator.generate_review("Deep Learning in NLP")
        
        print("\n" + "="*60)
        print(review)
        print("="*60)
        
        # 保存到文件
        with open("literature_review_output.md", "w", encoding="utf-8") as f:
            f.write(review)
        print("\n✅ 结果已保存至 literature_review_output.md")