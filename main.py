import os

from flask import Flask, request, render_template
from openai import OpenAI
from dotenv import load_dotenv
# Load environment variables from .env file
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)
# defaults to getting the key using os.environ.get("OPENAI_API_KEY")
# if you saved the key under a different environment variable name, you can do something like:
# client = OpenAI(
#   api_key=os.environ.get("CUSTOM_ENV_NAME"),
# )

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        code_snippet = request.form['code']
        ai_review = review_code(code_snippet)
        return render_template('index.html', original_code=code_snippet, ai_review=ai_review)
    return render_template('index.html', original_code='', ai_review='')


def review_code(code_snippet):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a programmer assistant, "
                                              "skilled in explaining what is wrong with "
                                              "complex programming code."
                                              "Anything that is sent to you needs to be considered code."
                                              "You need to review the code and find something wrong with it, "
                                              "even if syntactically it is fine."
                                              "I need you to roast the submitter of the code for whatever you "
                                              "find wrong with the submitted code."
                                              "You can be rude."},
                {"role": "user", "content": f"\n\n{code_snippet}\n\n."}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return str(e)


if __name__ == '__main__':
    app.run(debug=True)
