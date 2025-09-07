from .shared import AgentIO, tool_rules


SYSTEM = """You are the Writer Agent.
- Produce a structured article or report based on the analysis and sources.
- Include an executive summary, headings, and suggested images/charts.
- Tone should be adaptable; provide two variants: professional and conversational.
"""




def run(io: AgentIO) -> AgentIO:
analysis = io.data.get("analysis", "")
research = io.data.get("research", "")
prompt = f"Analysis:\n{analysis}\n\nSources:\n{research}\n\nReturn:\n- Executive summary (40-80 words)\n- 800-1000 word article with headings\n- Two-tone variants (professional & conversational)\n{tool_rules()}"
res = io.llm.complete(SYSTEM, prompt, max_tokens=1000)
io.data["article"] = res
return io