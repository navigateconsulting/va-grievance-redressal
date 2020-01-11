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
* provide_only_name{"complainant_city":"abc"}
  - utter_ask_mobile_and_email


##ask_city_if_not_provided_story
* provide_only_name{"complainant_name":"abc"}
  - utter_ask_city_if_not_provided
* provide_only_city{"complainant_name":"abc"}
  - utter_ask_mobile_and_email


##ask_normal_grievance_story
* provide_mobile_and_email{"complainant_name":"abc"}
  - utter_ask_grievance


##ask_email_ifnot_provided_story
* provide_only_mobile{"complainant_name":"abc"}
  - utter_ask_email_if_not_provided
* provide_only_email{"complainant_mobile":"987654310"}
  - utter_ask_grievance


##ask_mob_if_not_provided_story
* provide_only_email{"complainant_mobile":"987654310"}
  - utter_ask_mobile_if_not_provided
* provide_only_mobile{"complainant_email":"john.dow@xyz.com"}
  - utter_ask_grievance


##log_post_grievance_story
* ministry_of_railways_railway_board{"complainant_email":"john.dow@xyz.com"}
  - action_grievance_department


##los_grievance_issue_story_2
* ministry_of_railways_railway_board{"complainant_email":"john.dow@xyz.com"}
  - action_grievance_department


