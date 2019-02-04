# -*- coding: utf-8 -*-
import codecs
import os
import textwrap
import pathlib

from jinja2 import Template
from scrapy.exceptions import DropItem


class CleanPipeline(object):
    def process_item(self, item, spider):
        cleaned = self._clean(item)
        return cleaned

    def _clean(self, item):
        errors = []
        for field in 'number title difficulty cases solution'.split():
            if not item.get(field, None):
                errors.append(field)
        if errors:
            raise DropItem("Missing value(s) for %s in %s" % (", ".join(errors), item))

        item['number'] = item['number'].strip('#')
        item['cases'] = [case.strip() for case in item['cases']]
        return item


class MakeFourClojurePipeline(object):

    def process_item(self, item, spider):
        self._make_4clojure(item)
        return item

    clojure_code_dir = "four_clojure_tests"
    clojure_code_dir_skipped = "four_clojure_tests_skipped"
    clojure_code_dir_tofix = "four_clojure_tests_to_fix"

    clojure_template = """
        (ns four-clojure.problem-{{ number }}-test
          (:require [clojure.test :refer :all]))

        (declare __)

        (deftest problem-{{ number }}
          (testing "{{ title }}"
            {% for test in cases -%}
              (is {{ test }})
            {% endfor -%}
            ))

        (def __

          {{ solution|indent(10,False) }}

          )
    """

    def _make_4clojure(self, item):

        def format(item, template):
            rendered = Template(template).render(item)
            left_aligned = textwrap.dedent(rendered).strip()
            return left_aligned

        difficulty = item['difficulty']
        solution = item.get('solution', "")
        if difficulty == 'Elementary':
            directory = self.clojure_code_dir_skipped
        elif not (solution.rstrip().startswith("(") or solution.rstrip().startswith("#(")):
            directory = self.clojure_code_dir_tofix
        else:
            directory = self.clojure_code_dir

        code = format(item, self.clojure_template)
        number = item['number']
        pathlib.Path(directory).mkdir(parents=True, exist_ok=True)
        with codecs.open(os.path.join(directory, 'problem_{}_test.clj'.format(number)), 'w', 'utf8') as file:
            file.write(code)
