# 文献综述智能撰写多 Agent 系统

基于 LangChain + 智谱 AI (GLM-4) 构建的自动化文献综述生成系统。通过多 Agent 协作，自动完成文献检索、观点分析、逻辑梳理与格式排版。

## 项目结构

```
literature_review_agent/
├── main.py              # 主程序入口，包含完整的多 Agent 架构
├── requirements.txt     # Python 依赖项列表
└── README.md           # 项目说明文档
```

## 功能特点

- **多 Agent 流水线协作**：包含检索 Agent、分析 Agent、逻辑合成 Agent 和排版 Agent
- **基于 GLM-4 的长链推理**：利用智谱 AI 进行深度文献分析与综述撰写
- **结构化输出**：自动生成符合学术规范的 Markdown 格式文档

## 环境要求

- Python 3.9 或更高版本

## 安装与使用

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置 API Key

1.  访问 [智谱 AI 开放平台](https://open.bigmodel.cn/) 注册账号
2.  在控制台获取免费的 API Key
3.  打开 `main.py`，找到第 14 行，将 `your_zhipu_api_key_here` 替换为你的真实 Key

### 3. 运行程序

```bash
python main.py
```

### 4. 查看结果

- 程序会在控制台实时输出运行日志
- 生成的文献综述将自动保存为 `literature_review_output.md`

## 扩展说明

当前版本的文献检索为模拟数据。若需接入真实的文献数据库（如 IEEE Xplore、arXiv 或知网），请在 `LiteratureSearchAgent` 类中集成对应平台的 API。