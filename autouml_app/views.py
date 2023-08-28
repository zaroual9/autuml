import requests
import os
from django.shortcuts import render, redirect
from allauth.account.views import LoginView, LogoutView, SignupView
from django.contrib.auth.decorators import login_required
from django.conf import settings

class GPT:
    def __init__(self):
        self.url = "https://api.openai.com/v1/chat/completions"
        self.model = "gpt-3.5-turbo"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer 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"
        }
        self.prompt = "don't use !define or !include use just basic syntax in script"

    def ask(self, data, question):
        content = f"{self.prompt}\n\n{data}\n\n{question}"
        body = {
            "model": self.model,
            "messages": [{"role": "system", "content": "You are a helpful assistant."},
                         {"role": "user", "content": content}]
        }

        try:
            response = requests.post(url=self.url, headers=self.headers, json=body)
            response.raise_for_status()
            data = response.json()

            if "choices" in data and data["choices"]:
                return data["choices"][0]["message"]["content"]
            else:
                raise KeyError("Invalid response format: 'choices' key is missing or empty")
        except requests.exceptions.RequestException as e:
            print("An error occurred while making the API request:", e)
        except KeyError as e:
            print("Invalid response format:", e)
        except Exception as e:
            print("An error occurred:", e)

        return None

def extract_between_tags(input_content):
    try:
        start_index = input_content.find("@startuml")
        end_index = input_content.find("@enduml")

        if start_index != -1 and end_index != -1 and start_index < end_index:
            extracted_content = input_content[start_index:end_index+len("@enduml")]
            return extracted_content
        else:
            print("Start and end tags not found in the correct sequence.")
            return None
    except Exception as e:
        print("An error occurred:", e)
        return None

gpt = GPT()

@login_required
def generate_uml(request):
    if request.method == 'GET' and 'requirement' in request.GET:
        requirement = request.GET['requirement']
        uml_template =  " using PlantUML. Please avoid using !define or !include and instead use only basic syntax or create your custom nodes within the script." # Your UML template here
        
        # Generate UML code using GPT
        generated_code = gpt.ask(uml_template, requirement)
        extracted_uml = extract_between_tags(generated_code)

        if extracted_uml:
            user_id = request.user.id
            # Write UML code to a text file with user's ID in the filename
            uml_filename = os.path.join(settings.MEDIA_ROOT, f"uml_code_{user_id}.puml")
            with open(uml_filename, "w") as f:
                f.write(extracted_uml)

            # Use os.system to generate the diagram image
            os.system(f"python -m plantuml {uml_filename}")

            # Return the image filename
            image_filename = f"uml_code_{user_id}.png"
            return render(request, 'index.html', {'image_file': image_filename})

    return render(request, 'index.html', {'error': "Failed to generate UML code"})


class CustomLoginView(LoginView):
    template_name = 'login.html'

class CustomLogoutView(LogoutView):
    next_page = 'login'

class CustomSignupView(SignupView):
    template_name = 'signup.html'
