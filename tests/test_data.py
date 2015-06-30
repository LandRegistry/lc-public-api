import os

#open('filename.txt', 'r').read()
#dir = os.path.dirname(__file__)
#filename = os.path.join(dir, '/relative/path/to/file/you/want')

dir = os.path.dirname(__file__)

addr_withheld = open(os.path.join(dir, 'data/address_withheld.json'), 'r')



#debtor has residence withheld    address_withheld
# addr_withheld = '{"key_number": "2244098",' \
#  '"application_ref": "12345678",' \
#  '"date": "2015-06-16",' \
#  '"debtor_name": {' \
#      '"forenames": ["Roxane", "Sonia"],' \
#      '"surname": "Stracke"' \
#  '},' \
#  '"debtor_alternative_name": [{' \
#                                  '"forenames": ["Roxane"],' \
#                                  '"surname": "Bode"' \
#                              '}' \
#  '],' \
#  '"gender": "Not supplied",' \
#  '"occupation": "Distributed Goat Engineer",' \
#  '"trading_name": "Rox. Stracke",' \
#  '"residence": [],' \
#  '"residence_withheld": true,' \
#  '"date_of_birth": "1981-03-12",' \
#  '"investment_property": []' \
# '}'

#debtor has one residence and postcode    one_residence
residence_1 = '{ ' \
    '"key_number": "2244098",' \
    '"application_ref": "12345678",' \
    '"date": "2015-06-16",' \
    '"debtor_name": {' \
        '"forenames": ["Carolyne"],' \
        '"surname": "Greda"' \
    '},' \
    '"debtor_alternative_name": [],' \
    '"gender": "Not supplied",' \
    '"occupation": "Persistent Dynamic Modeller",' \
    '"trading_name": "Carolyne Fadel",' \
    '"residence": [{' \
                      '"address_lines": [' \
                          '"66543 Anabelle Path",' \
                          '"South Fosterfort"' \
                      '],' \
                      '"postcode": "PC12 3RR"' \
                  '}' \
    '],' \
    '"residence_withheld": false,' \
    '"date_of_birth": "1968-12-05",' \
    '"investment_property": []' \
'}'

#residence_withheld flag false but no address supplied    residence_withheld_false_no_address
withheld_flag_fail = '{ ' \
              '"key_number": "2244098",' \
              '"application_ref": "12345678",' \
              '"date": "2015-06-16",' \
              '"debtor_name": {' \
              '"forenames": ["Carolyne"],' \
              '"surname": "Greda"' \
              '},' \
              '"debtor_alternative_name": [],' \
              '"gender": "Not supplied",' \
              '"occupation": "Persistent Dynamic Modeller",' \
              '"trading_name": "Carolyne Fadel",' \
              '"residence": [] ,' \
              '"residence_withheld": false,' \
              '"date_of_birth": "1968-12-05",' \
              '"investment_property": []' \
              '}'

#debtor has 3 residences with 3 postcodes      three_residences
residence_3_pass = '{ ' \
              '"key_number": "2244098",' \
              '"application_ref": "12345678",' \
              '"date": "2015-06-16",' \
              '"debtor_name": {' \
              '"forenames": ["Carolyne", "Cremin"],' \
              '"surname": "Greda"' \
              '},' \
              '"debtor_alternative_name": [],' \
              '"gender": "Not supplied",' \
              '"occupation": "Persistent Dynamic Modeller",' \
              '"trading_name": "Carolyne Fadel",' \
              '"residence": [{' \
              '"address_lines": [' \
              '"66543 Anabelle Path",' \
              '"South Fosterfort"' \
              '],' \
              '"postcode": "PC12 3RR"' \
              '},' \
              '{' \
              '"address_lines": [' \
              '"63 New Road",' \
              '"South Fosterfort"' \
              '],' \
              '"postcode": "PC12 8RR"' \
              '},' \
               '{' \
               '"address_lines": [' \
               '"6 Main Street",' \
               '"South Fosterfort"' \
               '],' \
               '"postcode": "PC2 3RR"' \
               '}' \
               '],' \
              '"residence_withheld": false,' \
              '"date_of_birth": "1968-12-05",' \
              '"investment_property": []' \
              '}'

#debtor has 3 residence but only 2 postcodes  three_residences_one_missing_postcode
residence_3_fail = '{ ' \
                   '"key_number": "2244098",' \
                   '"application_ref": "12345678",' \
                   '"date": "2015-06-16",' \
                   '"debtor_name": {' \
                   '"forenames": ["Carolyne", "Cremin"],' \
                   '"surname": "Greda"' \
                   '},' \
                   '"debtor_alternative_name": [],' \
                   '"gender": "Not supplied",' \
                   '"occupation": "Persistent Dynamic Modeller",' \
                   '"trading_name": "Carolyne Fadel",' \
                   '"residence": [{' \
                   '"address_lines": [' \
                   '"66543 Anabelle Path",' \
                   '"South Fosterfort"' \
                   '],' \
                   '"postcode": "PC12 3RR"' \
                   '},' \
                   '{' \
                   '"address_lines": [' \
                   '"63 New Road",' \
                   '"South Fosterfort"' \
                   '],' \
                   '},' \
                   '{' \
                   '"address_lines": [' \
                   '"6 Main Street",' \
                   '"South Fosterfort"' \
                   '],' \
                   '"postcode": "PC2 3RR"' \
                   '}' \
                   '],' \
                   '"residence_withheld": false,' \
                   '"date_of_birth": "1968-12-05",' \
                   '"investment_property": []' \
                   '}'

#No key number supplied     no_key_number
no_key_no = '{ ' \
              '"application_ref": "12345678",' \
              '"date": "2015-06-16",' \
              '"debtor_name": {' \
              '"forenames": ["Carolyne", "Cremin"],' \
              '"surname": "Greda"' \
              '},' \
              '"debtor_alternative_name": [],' \
              '"gender": "Not supplied",' \
              '"occupation": "Persistent Dynamic Modeller",' \
              '"trading_name": "Carolyne Fadel",' \
              '"residence": [{' \
              '"address_lines": [' \
              '"66543 Anabelle Path",' \
              '"South Fosterfort"' \
              '],' \
              '"postcode": "PC12 3RR"' \
              '}' \
              '],' \
              '"residence_withheld": false,' \
              '"date_of_birth": "1968-12-05",' \
              '"investment_property": []' \
              '}'

#no reference supplied   no_reference
no_ref = '{ ' \
              '"key_number": "2244098",' \
              '"application_ref": ,' \
              '"date": "2015-06-16",' \
              '"debtor_name": {' \
              '"forenames": ["Carolyne", "Cremin"],' \
              '"surname": "Greda"' \
              '},' \
              '"debtor_alternative_name": [],' \
              '"gender": "Not supplied",' \
              '"occupation": "Persistent Dynamic Modeller",' \
              '"trading_name": "Carolyne Fadel",' \
              '"residence": [{' \
              '"address_lines": [' \
              '"66543 Anabelle Path",' \
              '"South Fosterfort"' \
              '],' \
              '"postcode": "PC12 3RR"' \
              '}' \
              '],' \
              '"residence_withheld": false,' \
              '"date_of_birth": "1968-12-05",' \
              '"investment_property": []' \
              '}'

no_date = '{ ' \
              '"key_number": "2244098",' \
              '"application_ref": "My reference",' \
              '"debtor_name": {' \
              '"forenames": ["Carolyne", "Cremin"],' \
              '"surname": "Greda"' \
              '},' \
              '"debtor_alternative_name": [],' \
              '"gender": "Not supplied",' \
              '"occupation": "Persistent Dynamic Modeller",' \
              '"trading_name": "Carolyne Fadel",' \
              '"residence": [{' \
              '"address_lines": [' \
              '"66543 Anabelle Path",' \
              '"South Fosterfort"' \
              '],' \
              '"postcode": "PC12 3RR"' \
              '}' \
              '],' \
              '"residence_withheld": false,' \
              '"date_of_birth": "1968-12-05",' \
              '"investment_property": []' \
              '}'

#no debtor name supplied  no_debtor_name
no_debtor_name = '{ ' \
              '"key_number": "2244098",' \
              '"application_ref": "12345678",' \
              '"date": "2015-06-16",' \
              '"debtor_alternative_name": [],' \
              '"gender": "Not supplied",' \
              '"occupation": "Persistent Dynamic Modeller",' \
              '"trading_name": "Carolyne Fadel",' \
              '"residence": [{' \
              '"address_lines": [' \
              '"66543 Anabelle Path",' \
              '"South Fosterfort"' \
              '],' \
              '"postcode": "PC12 3RR"' \
              '}' \
              '],' \
              '"residence_withheld": false,' \
              '"date_of_birth": "1968-12-05",' \
              '"investment_property": []' \
              '}'

#no debtor forename supplied    #no_debtor_forename
no_forename = '{ ' \
              '"key_number": "2244098",' \
              '"application_ref": "12345678",' \
              '"date": "2015-06-16",' \
              '"debtor_name": {' \
              '"surname": "Greda"' \
              '},' \
              '"debtor_alternative_name": [],' \
              '"gender": "Not supplied",' \
              '"occupation": "Persistent Dynamic Modeller",' \
              '"trading_name": "Carolyne Fadel",' \
              '"residence": [{' \
              '"address_lines": [' \
              '"66543 Anabelle Path",' \
              '"South Fosterfort"' \
              '],' \
              '"postcode": "PC12 3RR"' \
              '}' \
              '],' \
              '"residence_withheld": false,' \
              '"date_of_birth": "1968-12-05",' \
              '"investment_property": []' \
              '}'

#no debtor surname supplied   # no_debtor_surname
no_surname = '{ ' \
              '"key_number": "2244098",' \
              '"application_ref": "12345678",' \
              '"date": "2015-06-16",' \
              '"debtor_name": {' \
              '"forenames": ["Carolyne", "Cremin"],' \
              '},' \
              '"debtor_alternative_name": [],' \
              '"gender": "Not supplied",' \
              '"occupation": "Persistent Dynamic Modeller",' \
              '"trading_name": "Carolyne Fadel",' \
              '"residence": [{' \
              '"address_lines": [' \
              '"66543 Anabelle Path",' \
              '"South Fosterfort"' \
              '],' \
              '"postcode": "PC12 3RR"' \
              '}' \
              '],' \
              '"residence_withheld": false,' \
              '"date_of_birth": "1968-12-05",' \
              '"investment_property": []' \
              '}'

no_withheld_flag = '{ ' \
              '"key_number": "2244098",' \
              '"application_ref": "12345678",' \
              '"date": "2015-06-16",' \
              '"debtor_name": {' \
              '"forenames": ["Carolyne", "Cremin"],' \
              '"surname": "Greda"' \
              '},' \
              '"debtor_alternative_name": [],' \
              '"gender": "Not supplied",' \
              '"occupation": "Persistent Dynamic Modeller",' \
              '"trading_name": "Carolyne Fadel",' \
              '"residence": [{' \
              '"address_lines": [' \
              '"66543 Anabelle Path",' \
              '"South Fosterfort"' \
              '],' \
              '"postcode": "PC12 3RR"' \
              '}' \
              '],' \
              '"residence_withheld": ,' \
              '"date_of_birth": "1968-12-05",' \
              '"investment_property": []' \
              '}'

#debtor has 2 forenames and an alternative name  # debtor_2_names_alt.json
forename_2_alt_name = '{ ' \
              '"key_number": "2244098",' \
              '"application_ref": "12345678",' \
              '"date": "2015-06-16",' \
              '"debtor_name": {' \
              '"forenames": ["Carolyne", "Cremin"],' \
              '"surname": "Greda"' \
              '},' \
              '"debtor_alternative_name": [{' \
              '"forenames": ["Kerry","Mary"],' \
              '"surname": "Harris"' \
              '}'  \
              '],' \
              '"gender": "Not supplied",' \
              '"occupation": "Persistent Dynamic Modeller",' \
              '"trading_name": "Carolyne Fadel",' \
              '"residence": [{' \
              '"address_lines": [' \
              '"66543 Anabelle Path",' \
              '"South Fosterfort"' \
              '],' \
              '"postcode": "PC12 3RR"' \
              '}' \
              '],' \
              '"residence_withheld": false,' \
              '"date_of_birth": "1968-12-05",' \
              '"investment_property": []' \
              '}'

#debtor has 4 forenames and a surname  debtor_four_forenames
forename_4 = '{ ' \
              '"key_number": "2244098",' \
              '"application_ref": "12345678",' \
              '"date": "2015-06-16",' \
              '"debtor_name": {' \
              '"forenames": ["Carolyne","Joan","Lucy","Erica"],' \
              '"surname": "Greda"' \
              '},' \
              '"debtor_alternative_name": [],' \
              '"gender": "Not supplied",' \
              '"occupation": "Persistent Dynamic Modeller",' \
              '"trading_name": "Carolyne Fadel",' \
              '"residence": [{' \
              '"address_lines": [' \
              '"66543 Anabelle Path",' \
              '"South Fosterfort"' \
              '],' \
              '"postcode": "PC12 3RR"' \
              '}' \
              '],' \
              '"residence_withheld": false,' \
              '"date_of_birth": "1968-12-05",' \
              '"investment_property": []' \
              '}'

no_gender = '{ ' \
              '"key_number": "2244098",' \
              '"application_ref": "12345678",' \
              '"date": "2015-06-16",' \
              '"debtor_name": {' \
              '"forenames": ["Carolyne"],' \
              '"surname": "Greda"' \
              '},' \
              '"debtor_alternative_name": [],' \
              '"occupation": "Persistent Dynamic Modeller",' \
              '"trading_name": "Carolyne Fadel",' \
              '"residence": [{' \
              '"address_lines": [' \
              '"66543 Anabelle Path",' \
              '"South Fosterfort"' \
              '],' \
              '"postcode": "PC12 3RR"' \
              '}' \
              '],' \
              '"residence_withheld": false,' \
              '"date_of_birth": "1968-12-05",' \
              '"investment_property": []' \
              '}'

no_occupation = '{ ' \
              '"key_number": "2244098",' \
              '"application_ref": "12345678",' \
              '"date": "2015-06-16",' \
              '"debtor_name": {' \
              '"forenames": ["Carolyne"],' \
              '"surname": "Greda"' \
              '},' \
              '"debtor_alternative_name": [],' \
              '"gender": "Not supplied",' \
              '"trading_name": "Carolyne Fadel",' \
              '"residence": [{' \
              '"address_lines": [' \
              '"66543 Anabelle Path",' \
              '"South Fosterfort"' \
              '],' \
              '"postcode": "PC12 3RR"' \
              '}' \
              '],' \
              '"residence_withheld": false,' \
              '"date_of_birth": "1968-12-05",' \
              '"investment_property": []' \
              '}'

no_trading_name = '{ ' \
              '"key_number": "2244098",' \
              '"application_ref": "12345678",' \
              '"date": "2015-06-16",' \
              '"debtor_name": {' \
              '"forenames": ["Carolyne"],' \
              '"surname": "Greda"' \
              '},' \
              '"debtor_alternative_name": [],' \
              '"gender": "Not supplied",' \
              '"occupation": "Persistent Dynamic Modeller",' \
              '"residence": [{' \
              '"address_lines": [' \
              '"66543 Anabelle Path",' \
              '"South Fosterfort"' \
              '],' \
              '"postcode": "PC12 3RR"' \
              '}' \
              '],' \
              '"residence_withheld": false,' \
              '"date_of_birth": "1968-12-05",' \
              '"investment_property": []' \
              '}'

all_fields = '{"key_number": "2244098",' \
              '"application_ref": "12345678",' \
              '"date": "2015-06-16",' \
              '"debtor_name": {' \
                  '"forenames": ["Carolyne"],' \
                  '"surname": "Greda"' \
              '},' \
              '"debtor_alternative_name": [{' \
                                              '"forenames": ["Kerry","Mary"],' \
                                              '"surname": "Harris"' \
                                          '}' \
              '],' \
              '"gender": "Neuter",' \
              '"occupation": "Persistent Dynamic Modeller",' \
              '"trading_name": "Carolyne Fadel",' \
              '"residence": [{' \
                                '"address_lines": [' \
                                    '"66543 Anabelle Path",' \
                                    '"South Fosterfort"' \
                                '],' \
                                '"postcode": "PC12 3RR"' \
                            '}' \
              '],' \
              '"residence_withheld": false,' \
              '"buisness_address":[{' \
                                      '"address_lines": [' \
                                          '"66 Industrial Road",' \
                                          '"South Fosterfort"' \
                                      '],' \
                                      '"postcode": "PC12 3RR"' \
                                  '},' \
                                  '{' \
                                      '"address_lines": [' \
                                          '"63 New Road",' \
                                          '"South Fosterfort"' \
                                      '],' \
                                      '"postcode": "PC12 8RR"' \
                                  '},' \
                                  '{' \
                                      '"address_lines": [' \
                                          '"6 Main Street",' \
                                          '"South Fosterfort"' \
                                      '],' \
                                      '"postcode": "PC2 3RR"' \
                                  '}' \
              '],' \
              '"date_of_birth": "1968-12-05",' \
              '"investment_property": [{' \
                                          '"address_lines": [' \
                                              '"66 Industrial Road",' \
                                              '"South Fosterfort"' \
                                          '],' \
                                          '"postcode": "PC12 3RR"' \
                                      '},' \
                                      '{' \
                                          '"address_lines": [' \
                                              '"63 New Road",' \
                                              '"South Fosterfort"' \
                                          '],' \
                                          '"postcode": "PC12 8RR"' \
                                      '},' \
                                      '{' \
                                          '"address_lines": [' \
                                              '"6 Main Street",' \
                                              '"South Fosterfort"' \
                                          '],' \
                                          '"postcode": "PC2 3RR"' \
                                      '}' \
              ']' \
              '}' \






