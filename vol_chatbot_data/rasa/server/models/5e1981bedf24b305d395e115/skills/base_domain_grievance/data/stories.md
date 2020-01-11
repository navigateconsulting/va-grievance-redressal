##greet_story
* greet
  - utter_greet


##greet_and_basic_info_story
* greet
  - utter_greet
* provide_name_and_city
  - utter_ask_mobile_and_email


##basic_and_contact_info_story
* provide_name_and_city
  - utter_ask_mobile_and_email
* provide_mobile_and_email
  - utter_ask_grievance


##ask_name_if_not_provided_story
* provide_only_city
  - utter_ask_name_if_not_provided
* provide_only_name
  - utter_ask_mobile_and_email


##ask_city_if_not_provided_story
* provide_only_name
  - utter_ask_city_if_not_provided
* provide_only_city
  - utter_ask_mobile_and_email


##ask_normal_grievance_story
* provide_mobile_and_email
  - utter_ask_grievance


##ask_email_ifnot_provided_story
* provide_only_mobile
  - utter_ask_email_if_not_provided
* provide_only_email
  - utter_ask_grievance


##ask_mob_if_not_provided_story
* provide_only_email
  - utter_ask_mobile_if_not_provided
* provide_only_mobile
  - utter_ask_grievance


##log_post_grievance_story
* department_of_posts
  - action_grievance_department


##los_grievance_issue_story_2
* department_of_posts
  - action_grievance_department


##log_railway_grievance_story
* ministry_of_railways_railway_board
  - action_grievance_department


##log_railway_grievance_story_2
* ministry_of_railways_railway_board
  - action_grievance_department


##log_tax_grievance_story
* central_board_of_direct_taxes_income_tax
  - action_grievance_department


##log_tax_grievance_story_2
* central_board_of_direct_taxes_income_tax
  - action_grievance_department


##log_finance_grievance_story
* central_board_of_direct_taxes_income_tax
  - action_grievance_department


##log_finance_grievance_story_2
* department_of_financial_services_banking_division
  - action_grievance_department


##log_telecom_grievance_story
* department_of_telecommunications
  - action_grievance_department


##log_telecom_grievance_story_2
* department_of_telecommunications
  - action_grievance_department


