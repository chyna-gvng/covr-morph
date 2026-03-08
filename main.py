import pymupdf4llm
import os
import tomllib
from smolagents import ToolCallingAgent, LiteLLMModel
from selector import get_context
from weasyprint import HTML
from jinja2 import Template
from models import CV

with open("prompts.toml", "rb") as f:
    PROMPTS = tomllib.load(f)


def run_cv_tailor(cv_path="data/my-cv.pdf", jd_path="data/jd.txt"):
    if not os.path.exists(jd_path):
        print(f"Error: {jd_path} not found.")
        return

    print("📄 Parsing CV and loading Job Description...")
    cv_markdown = pymupdf4llm.to_markdown(cv_path)
    with open(jd_path, "r") as f:
        job_description = f.read()

    style_context = get_context(job_description)

    model = LiteLLMModel(
        model_id="openrouter/openai/gpt-4o",
        api_key=os.getenv("OPENROUTER_API_KEY"),
        response_format=CV,
    )

    agent = ToolCallingAgent(
        model=model, tools=[], instructions=PROMPTS["system"]["instructions"]
    )

    prompt = PROMPTS["task"]["template"].format(
        cv_content=cv_markdown,
        job_description=job_description,
        style_guide=style_context["context"],
    )

    print("🤖 Requesting structured output from gpt-4o...")
    raw_response = agent.run(prompt)

    try:
        cv_data = CV.model_validate_json(str(raw_response))

        for s in cv_data.skills:
            if not s.items or s.items == s.category:
                print(f"⚠️ Warning: {s.category} has empty or invalid items.")

        with open("template.html", "r") as f:
            template_content = f.read()

        jinja_template = Template(template_content)
        rendered_html = jinja_template.render(
            personal=cv_data.personal.model_dump(),
            summary=cv_data.summary,
            education=[e.model_dump() for e in cv_data.education],
            experience=[e.model_dump() for e in cv_data.experience],
            projects=[p.model_dump() for p in cv_data.projects],
            skills=[s.model_dump() for s in cv_data.skills],
            honours_awards=[h.model_dump() for h in cv_data.honours_awards],
            publications=[p.model_dump() for p in cv_data.publications],
            references=[r.model_dump() for r in cv_data.references],
        )

        output_filename = "data/output-cv.pdf"

        print(f"🎨 Rendering PDF: {output_filename}")
        HTML(string=rendered_html).write_pdf(output_filename)
        print("✅ Success!")

    except Exception as e:
        print(f"❌ An error occurred: {e}")


if __name__ == "__main__":
    run_cv_tailor()
