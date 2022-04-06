# -*- coding: utf-8 -*-
#
# RERO ILS
# Copyright (C) 2022 RERO
# Copyright (C) 2022 UCLouvain
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""Tests Serializers."""

from rero_ils.modules.documents.serializers.ris import RISFormatter

es_record = {
  "pid": "945",
  "type": [
    {
      "main_type": "docmaintype_audio",
      "subtype": "docsubtype_music"
    },
    {
      "main_type": "docmaintype_audio",
      "subtype": "docsubtype_sound"
    }
  ],
  "language": [
    {
      "type": "bf:Language",
      "value": "fre"
    },
    {
      "type": "bf:Language",
      "value": "ita"
    }
  ],
  "title": [
    {
      "_text": "Immigration : quelle intégration ? Quels droits politiques ?."
               " Immigrazione : quale integrazione? Quali diritti politichi?",
      "mainTitle": [
        {
          "value": "Immigration"
        }
      ],
      "subtitle": [
        {
          "value": "quelle intégration ? Quels droits politiques ?"
        }
      ],
      "type": "bf:Title"
    },
    {
      "_text": "Immigration : quelle intégration ? Quels droits politiques ?."
               " Immigrazione : quale integrazione? Quali diritti politichi?",
      "mainTitle": [
        {
          "value": "Immigrazione"
        }
      ],
      "subtitle": [
        {
          "value": "quale integrazione? Quali diritti politichi?"
        }
      ],
      "type": "bf:ParallelTitle"
    },
    {
      "partOfTitle": [
        {
          "value": "Scrittori e scritture"
        }
      ],
      "type": "partOf"
    }
  ],
  "contribution": [
    {
      "agent": {
        "date_of_birth": "1921",
        "date_of_death": "1987",
        "numeration": "XXII",
        "preferred_name": "Yourcenar, Marguerite",
        "qualifier": "autrice",
        "type": "bf:Person"
      },
      "role": [
        "abr"
      ]
    },
    {
      "agent": {
        "conference": False,
        "preferred_name": "Université de Genève",
        "subordinate_unit": [
          "Faculté des sciences"
        ],
        "type": "bf:Organisation"
      },
      "role": [
        "aut"
      ]
    },
    {
      "agent": {
        "authorized_access_point_de": "Morante, Elsa, 1912-1985",
        "authorized_access_point_en": "Morante, Elsa, 1912-1985",
        "authorized_access_point_fr": "Morante, Elsa, 1912-1985",
        "authorized_access_point_it": "Morante, Elsa, 1912-1985",
        "parallel_access_point": [
          "Morante, Elsa, 1912-1985"
        ],
        "pid": "1664490",
        "type": "bf:Person",
        "variant_access_point": [
          "Morante, Ėl'za, 1912-1985",
          "מורנטה, אלזה, 1912-1985"
        ]
      },
      "role": [
        "cre"
      ]
    },
    {
      "agent": {
        "authorized_access_point_de": "Garboli, Cesare, 1928-2004",
        "authorized_access_point_en": "Garboli, Cesare, 1928-2004",
        "authorized_access_point_fr": "Garboli, Cesare, 1928-2004",
        "authorized_access_point_it": "Garboli, Cesare, 1928-2004",
        "pid": "4575430",
        "type": "bf:Person",
        "variant_access_point": [
          "Gàrboli, Cesare, 1928-2004"
        ]
      },
      "role": [
        "ctb"
      ]
    }
  ],
  "identifiedBy": [
    {
      "type": "bf:Doi",
      "value": "10.1530/eje-20-0380e"
    },
    {
      "type": "bf:Isbn",
      "value": "9782755507171"
    },
    {
      "type": "bf:Issn",
      "value": "0254-6523"
    },
    {
      "source": "RERO",
      "type": "bf:Local",
      "value": "R008128420"
    }
  ],
  "editionStatement": [
    {
      "_text": "Révisé, corrigé et augmenté / par Emile Chatelain",
      "editionDesignation": "Révisé, corrigé et augmenté",
      "responsibility": "par Emile Chatelain"
    }
  ],
  "provisionActivity": [
    {
      "type": "bf:Publication",
      "startDate": "1866",
      "endDate": "1944",
      "place": [
        {
          "country": "sz",
          "canton": "ne",
          "type": "bf:Place",
          "$ref": "link to MEF"
        }
      ],
      "statement": [
        {
          "label": [
            {
              "value": "Neuchâtel, La Chaux-de-Fonds [ou] Colombier"
            }
          ],
          "type": "bf:Place"
        },
        {
          "label": [
            {
              "value": "Club jurassien, [puis] A. Mathey-Dupraz"
            }
          ],
          "type": "bf:Agent"
        },
        {
          "label": [
            {
              "value": "Place 2"
            }
          ],
          "type": "bf:Place"
        },
        {
          "label": [
            {
              "value": "Publisher 2"
            }
          ],
          "type": "bf:Agent"
        },
        {
          "label": [
            {
              "value": "1866-1944"
            }
          ],
          "type": "Date"
        }
      ]
    },
    {
      "_text": [
        {
          "language": "default",
          "value": "58-Clamecy : Impr. Laballery"
        }
      ],
      "statement": [
        {
          "label": [
            {
              "value": "58-Clamecy"
            }
          ],
          "type": "bf:Place"
        },
        {
          "label": [
            {
              "value": "Impr. Laballery"
            }
          ],
          "type": "bf:Agent"
        }
      ],
      "type": "bf:Manufacture"
    }
  ],
  "extent": "17 p.",
  "partOf": [
    {
      "document": {
        "$ref": "https://bib.rero.ch/api/documents/doc1"
      },
      "numbering": [
        {
          "issue": 5,
          "pages": "22-928",
          "volume": 3,
          "year": "1988"
        },
        {
          "issue": 8,
          "pages": "42",
          "volume": 6,
          "year": "1998"
        }
      ]
    }
  ],
  "seriesStatement": [
    {
      "_text": [
        {
          "language": "default",
          "value": "Collection Savoir"
        }
      ],
      "seriesTitle": [
        {
          "value": "Collection Savoir"
        }
      ]
    }
  ],
  "electronicLocator": [
    {
      "content": "audio",
      "type": "resource",
      "url": "https://mediatheque.ch/html/lien1.pdf"
    },
    {
      "type": "versionOfResource",
      "url": "https://mediatheque.ch/html/lien2.pdf"
    }
  ],
  "subjects": [
    {
      "type": "bf:Person",
      "gnd": {
        "authorized_access_point": "Aristoteles, v384-v322"
      }
    },
    {
      "type": "bf:Person",
      "idref": {
        "authorized_access_point": "Montagnier, Jean-Paul, 1965-...."
      },
      "rero": {
        "authorized_access_point": "Montagnier, Jean-Paul, 1965-"
      }
    },
    {
      "type": "bf:Person",
      "preferred_name": "Athenagoras (patriarche oecuménique ; 1)",
      "identifiedBy": {
        "value": "A009963344",
        "source": "rero",
        "type": "bf:Local"
      },
      "source": "rero"
    },
    {
      "type": "bf:Place",
      "preferred_name": "Europe occidentale",
      "identifiedBy": {
        "value": "A009975209",
        "source": "rero",
        "type": "bf:Local"
      },
      "source": "rero"
    },
    {
      "type": "bf:Topic",
      "term": "Bases de données",
      "identifiedBy": {
        "value": "A001234567",
        "source": "rero",
        "type": "bf:Local"
      },
      "source": "rero"
    },
    {
      "creator": "Voltenauer, Marc",
      "identifiedBy": {
        "type": "RERO",
        "value": "A001234567"
      },
      "source": "rero",
      "title": "Bases de données",
      "type": "bf:Work"
    }
  ]
}


def test_ris_formatter(client):
    """Test RIS formatter"""
    ris_tag = [
        'TY -', 'ID -', 'TI -', 'T2 -', 'AU -', 'A2 -', 'DA -', 'SP -', 'EP -',
        'CY -', 'LA -', 'PB -', 'SN -', 'UR -', 'KW -', 'ET -', 'DO -', 'VL -',
        'IS -', 'PP -', 'Y1 -', 'PY -', 'ER -'
    ]
    formatter = RISFormatter(es_record)
    ris_data = formatter.format()

    assert all(tag in ris_data for tag in ris_tag)
