from openai import OpenAI
from openai.types.chat import ChatCompletionToolParam
import os
from dotenv import load_dotenv

import base64
load_dotenv()


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

client = OpenAI(
    api_key = os.getenv("OPENAI_API_KEY")
)

tools = [{ 
    "type": "function",
    "name": "payslip_parser",
    "description": "Given the input image which is a payslip, dissect it into the parameters given.",
    "parameters": {
        "type": "object",
        "properties": {
            "pay_date": {
                "type": "string",
                "format": "date"
            },
            "amount": {"type": "number"},
            "additions": {
                "type": "object",
                "description": "Dictionary of optional additional payments (e.g., bonuses, reimbursements)",
                "additionalProperties": { "type": "number" }
            },
            "deductions": {
                "type": "object",
                "description": "Optional deductions such as stock purchase plans",
                "additionalProperties": { "type": "number" }
            },
            "taxable_income": {"type": "number"},
            "taxable_income_ytd": {"type": "number"},
            "additions_after_tax": {"type": "number"},
            "additions_after_tax_ytd": {"type": "number"},
            "gross": {"type": "number"},
            "gross_ytd": {"type": "number"},
            "tax": {"type": "number"},
            "tax_ytd": {"type": "number"},
            "deductions_after_tax": {"type": "number"},
            "deductions_after_tax_ytd": {"type": "number"},
            "net_pay": {"type": "number"},
            "net_pay_ytd": {"type": "number"},
            "superannuation":{"type": "number"},
            "superannuation_ytd":{"type": "number"},
            "annual_salary_ytd":{"type": "number"},
            "STSL": {"type": "number"}
        },
        "required": [
            "pay_date", 
            "amount", 
            "taxable_income", 
            "taxable_income_ytd", 
            "additions_after_tax",
            "additions_after_tax_ytd",
            "gross",
            "gross_ytd",
            "tax",
            "tax_ytd",
            "deductions_after_tax",
            "deductions_after_tax_ytd",
            "net_pay",
            "net_pay_ytd",
            "superannuation",
            "superannuation_ytd",
            "annual_salary_ytd",
            "STSL"
        ],
        "additionalProperties": False
    }
}]


# upload payslip
payslip_path="payslip_2025-04.png"
base64_image = encode_image(payslip_path)


# image_file = client.files.create(
#     file=open(payslip_path, "rb"),
#     purpose="vision"
# )


# response = client.responses.create(
#     model="gpt-4.1-mini",
#     input=[
#         {
#             "role": "user",
#             "content": [
#                 {"type": "input_text", "text": "Extract payslip details and return them in structured format."},
#                 {
#                     "type": "input_image",
#                     "image_url": f"data:image/png;base64,{base64_image}",
#                 },
#             ],
#         } # type: ignore
#     ], 
#     tools=tools, # type: ignore
#     store=False,
#     max_output_tokens=2048
# )

completion = client.chat.completions.create(
    model="gpt-4.1-mini",
    messages=[
        {
            "role": "user",
            "content": [
                { "type": "text", "text": "Extract payslip details and return them in structured format." },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image}",
                    },
                },
            ],
        }
    ],
)
# response = client.responses.create(
#     model="gpt-4.1-mini",
#     input=[
#         {
#             "role": "user",
#             "content": [
#                 {"type": "input_text", "text": "Extract payslip details and return them in structured format."},
#                 {
#                     "type": "input_image",
#                     "image_url": f"data:image/png;base64,{base64_image}",
#                 },
#             ],
#         } # type: ignore
#     ], 
#     tools=tools, # type: ignore
#     store=False,
#     max_output_tokens=2048
# )
# print(response.usage.input_tokens)       # tokens in input
# print(response.usage.output_tokens)   # tokens in outputns 
#print(response.output)

print(completion.choices[0].message.content)
print(completion.usage.prompt_tokens) # type: ignore
print(completion.usage.completion_tokens) # type: ignore

# https://platform.openai.com/docs/guides/images?api-mode=chat&format=base64-encoded#provide-multiple-image-inputs

del client