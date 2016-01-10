import jinja2
from mongo_functions import getTemplateContext
import io


def renderTemplate(name):
    templateLoader = jinja2.FileSystemLoader(searchpath='templates')
    templateEnv = jinja2.Environment(loader=templateLoader)

    template = templateEnv.get_template("template.html")

    # call getTemplateContext function which is returns context from mongodb
    context = getTemplateContext()
    context['name'] = name

    renderedTemplate = template.render(context)

    email = io.open('scripts/rendered_templates/rendered.html', 'w', encoding='ascii', errors="ignore")
    email.write(renderedTemplate)
    email.close()


if __name__ == '__main__':
    renderTemplate("Called from the CLI")
