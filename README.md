# 🤖 ScholarAgent - 智能科研论文分析助手

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![LangChain](https://img.shields.io/badge/LangChain-0.1.0-green.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28.1-red.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![DeepSeek](https://img.shields.io/badge/DeepSeek-API-orange.svg)

**基于LangChain + ReAct Agent的智能科研论文分析助手**

[🚀 快速开始](#-快速开始) • [✨ 功能特性](#-功能特性) • [📖 使用示例](#-使用示例) • [🔧 安装配置](#-安装配置) • [🎯 应用场景](#-应用场景)

</div>

---

## 📖 项目简介

ScholarAgent是一个基于大语言模型的智能科研论文分析助手，采用ReAct（Reasoning and Acting）推理策略，能够自主规划任务执行流程，调用各种工具完成论文检索、总结和问答任务。

### 🎯 核心价值

- **🔍 智能检索**：快速找到相关论文，支持多种搜索方式
- **📝 深度分析**：自动总结论文贡献、方法、创新点
- **💬 智能问答**：基于论文内容回答专业问题
- **🧠 上下文记忆**：支持多轮对话，理解指代表达
- **🔗 便捷访问**：自动提供arXiv ID和PDF链接

---

## ✨ 功能特性

### 🤖 智能Agent架构
- **ReAct推理框架**：基于LangChain的推理和行动架构
- **自主任务规划**：智能分析用户需求，自动选择合适工具
- **多工具集成**：无缝集成Arxiv API和LLM服务

### 🔍 论文检索功能
- **多维度搜索**：支持按标题、作者、关键词搜索
- **结构化输出**：包含标题、作者、摘要、arXiv ID、PDF链接
- **批量处理**：支持多篇论文同时检索和展示

### 📊 智能分析功能
- **研究贡献总结**：自动分析论文的研究问题和主要贡献
- **技术方法分析**：深入分析技术框架和算法方法
- **论文比较**：智能比较多篇论文的异同点
- **关键点提取**：自动提取论文核心信息

### 💬 上下文记忆
- **对话历史**：完整保存多轮对话内容
- **论文缓存**：自动缓存搜索到的论文信息
- **指代理解**：智能理解"这篇论文"、"作者"等指代表达
- **上下文增强**：自动补充相关上下文信息

### 🌐 双界面支持
- **命令行界面**：轻量级交互式命令行应用
- **Streamlit界面**：现代化Web界面，支持可视化展示

---

## 🚀 快速开始

### 1. 环境要求

- Python 3.8+
- DeepSeek API密钥
- 稳定的网络连接

### 2. 安装配置

```bash
# 克隆项目
git clone https://github.com/LBJ-mlo/ScholarAgent.git
cd ScholarAgent

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp env_example.txt .env
```

编辑 `.env` 文件，填入您的API密钥：
```bash
DEEPSEEK_API_KEY=your_deepseek_api_key_here
DEEPSEEK_BASE_URL=https://api.deepseek.com/v1
DEEPSEEK_MODEL=deepseek-chat
```

### 3. 运行应用

```bash
# 命令行模式（推荐）
python app.py

# Web界面模式
streamlit run ui/streamlit_app.py
```

---

## 📖 使用示例

### 🔍 搜索论文

```python
from agent.controller import run_agent

# 搜索论文
result = run_agent("请搜索论文 Segment Anything")
print(result)
```

**输出示例：**
```
我找到了Segment Anything论文的详细信息：

论文标题: Segment Anything
作者: Alexander Kirillov, Eric Mintun, Nikhila Ravi, ...
Arxiv ID: 2304.02643
发布日期: 2023-04-05
分类: cs.CV (计算机视觉)
PDF链接: https://arxiv.org/pdf/2304.02643.pdf

摘要: We present the Segment Anything (SA) project: a new task, model, and dataset for image segmentation...

arXiv ID: 2304.02643
PDF链接: http://arxiv.org/pdf/2304.02643
```

### 📝 总结论文贡献

```python
from agent.controller import create_scholar_agent

agent = create_scholar_agent()
result = agent.summarize_paper("Segment Anything")
print(result["answer"])
```

**输出示例：**
```
基于对Segment Anything论文的分析，该论文的主要研究贡献包括：

## 研究问题
提出了Segment Anything (SA)项目，这是一个新的图像分割任务、模型和数据集...

## 主要贡献
1. 大规模数据集构建：构建了迄今为止最大的分割数据集SA-1B...
2. 高效提示式模型：提出了一个高效的提示式分割模型...
3. 通用分割框架：设计了可提示的模型架构...
```

### 💬 智能问答

```python
# 回答具体问题
result = agent.answer_question("这篇论文的主要技术方法是什么？", "Segment Anything")
print(result["answer"])

# 多轮对话
result1 = agent.run("搜索论文 Attention Is All You Need")
result2 = agent.run("这篇论文的作者是谁？")  # 自动理解指代
```

### 🔄 论文比较

```python
result = agent.compare_papers("Segment Anything", "Attention Is All You Need")
print(result["answer"])
```

---
<img width="2401" height="1321" alt="image" src="https://github.com/user-attachments/assets/eb732181-cb3e-46ec-b015-fe60f3a069d4" />
## 🎯 应用场景

### 👨‍🎓 学生群体
- **论文学习**：快速理解复杂论文内容
- **文献调研**：高效进行学术研究
- **写作辅助**：获取论文写作灵感

### 👨‍🔬 科研人员
- **文献检索**：快速找到相关研究
- **趋势分析**：了解研究领域发展
- **方法比较**：分析不同技术方案

### 📚 学术写作
- **文献综述**：辅助撰写文献综述
- **引用分析**：了解论文引用关系
- **创新点挖掘**：发现研究创新点

### 🏫 教育机构
- **课程辅助**：辅助教学和课程设计
- **研究指导**：指导学生进行研究
- **学术交流**：促进学术交流合作

---

## 🏗️ 技术架构

```
ScholarAgent/
├── agent/                 # Agent核心模块
│   ├── controller.py     # ReAct Agent控制器
│   ├── tools.py          # LangChain工具定义
│   └── prompts.py        # 提示词模板
├── services/             # 服务层
│   ├── search.py         # Arxiv搜索服务
│   └── summarize.py      # LLM总结服务
├── ui/                   # 用户界面
│   └── streamlit_app.py  # Streamlit Web界面
├── config.py            # 配置管理
├── app.py               # 命令行入口
├── requirements.txt     # 依赖包
├── .gitignore          # Git忽略文件
├── env_example.txt     # 环境变量示例
└── README.md           # 项目文档
```

### 🔧 核心技术栈

| 技术 | 版本 | 用途 |
|------|------|------|
| Python | 3.8+ | 主要开发语言 |
| LangChain | 0.1.0 | Agent框架 |
| DeepSeek API | - | LLM服务 |
| Arxiv API | - | 论文检索 |
| Streamlit | 1.28.1 | Web界面 |
| python-dotenv | 1.0.0 | 环境变量管理 |

---

## 🔧 可用工具

ScholarAgent集成了以下智能工具：

### 1. 🔍 search_arxiv - 论文搜索
- **功能**：Arxiv论文搜索
- **支持**：按标题、作者、关键词搜索
- **输出**：论文详细信息

### 2. 📝 summarize_contributions - 贡献总结
- **功能**：总结研究贡献
- **分析**：研究问题、主要贡献、创新点
- **输出**：结构化总结报告

### 3. 🔬 summarize_methods - 方法分析
- **功能**：总结技术方法
- **分析**：技术框架、算法方法
- **评估**：技术优势和适用场景

### 4. 💬 answer_question - 智能问答
- **功能**：基于论文内容回答用户问题
- **支持**：上下文理解
- **特点**：专业、准确、详细

### 5. 🎯 generate_key_points - 关键点提取
- **功能**：提取论文核心信息点
- **输出**：简洁的要点总结
- **应用**：快速了解论文重点

### 6. ⚖️ compare_papers - 论文比较
- **功能**：比较两篇论文的异同点
- **维度**：研究问题、方法、创新点、应用场景
- **输出**：详细比较分析

---

## 🚀 部署选项

### 本地部署
```bash
# 克隆并安装
git clone https://github.com/LBJ-mlo/ScholarAgent.git
cd ScholarAgent
pip install -r requirements.txt

# 配置并运行
cp env_example.txt .env
# 编辑.env文件
python app.py
```

### Docker部署
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "ui/streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### 云平台部署
- **Streamlit Cloud**：一键部署Web应用
- **Heroku**：支持Procfile部署
- **Vercel**：支持Python应用部署

---

## 🤝 贡献指南

我们欢迎所有形式的贡献！

### 🐛 报告问题
如果您发现了bug或有功能建议，请[创建Issue](https://github.com/LBJ-mlo/ScholarAgent/issues)。


---

## 📄 许可证

本项目采用MIT许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

---

## 🙏 致谢

- **LangChain团队**：提供了优秀的Agent框架
- **DeepSeek团队**：提供了强大的LLM服务
- **Arxiv团队**：提供了开放的论文API
- **Streamlit团队**：提供了便捷的Web框架

---

## 📞 联系我们

- **GitHub Issues**: [https://github.com/LBJ-mlo/ScholarAgent/issues](https://github.com/LBJ-mlo/ScholarAgent/issues)
- **项目主页**: [https://github.com/LBJ-mlo/ScholarAgent](https://github.com/LBJ-mlo/ScholarAgent)

---

<div align="center">

**⭐ 如果这个项目对您有帮助，请给我们一个Star！**

Made with ❤️ by [LBJ-mlo](https://github.com/LBJ-mlo)

</div> 
