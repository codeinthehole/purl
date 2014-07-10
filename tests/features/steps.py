from lettuce import *

import purl


@step("I have the template '(.*)'")
def have_a_template(step, template):
    world.template = purl.Template(template)

@step("I expand it")
def expand_template(step):
    world.url = world.template.expand()

@step("I see an empty string")
def check_url(step):
    assert "" == world.url.as_string()
