def get_camps_form(google, sf, title, week_codes):
    result = google.create_camps_form()

    def get_camp_texts(week_code):
        camp_codes = sf.get_camps_per_week(week_code, confirmed="Not Cancelled")

        def get_camp_text(camp_code):
            return sf.get_camp_details(camp_code)["teacher_text"]

        camp_texts = [get_camp_text(camp_code) for camp_code in camp_codes]

        return camp_texts

    camp_texts = [get_camp_texts(week_code) for week_code in week_codes]

    # Check all entries of camp_texts are not empty
    if not all([camp_texts]):
        raise ValueError("[ERROR] All week lists must be non-empty")

    update = {
        "requests": [
            {
                "createItem": {
                    "item": {
                        "title": sf.get_week_long_name(week_code),
                        "questionItem": {
                            "question": {
                                "choiceQuestion": {
                                    "type": "CHECKBOX",
                                    "options": [
                                        {"value": camp_text} for camp_text in camp_texts[i]
                                    ]
                                }
                            }
                        },
                    },
                    "location": {"index": 5 + i},
                }
            }
            for i, week_code in enumerate(week_codes)]
    }
    update["requests"].append({
        "updateFormInfo": {
            "info": {
                "title": title
            },
            "updateMask": "title",
        }
    })

    form_id = result["id"]
    google.update_form(form_id, update)
    google.publish_form(form_id)

    editor_uri = f"https://docs.google.com/forms/d/{form_id}/edit"
    print(f'[SUCCESS] Form created successfully under link {editor_uri}')
    return editor_uri
