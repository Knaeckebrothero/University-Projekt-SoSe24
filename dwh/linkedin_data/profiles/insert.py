"""
This module holds the functions used to import the individual attributes into the DWH.
"""
import pandas as pd
import sqlalchemy  # Requires pymysql
from datetime import datetime
# Import conversion functions
from dwh.linkedin_data.profiles import convert as conv


def location(document: dict, dwh_engine) -> int:
    """
    This function inserts a location into the DWH and returns its ID.

    DWH table: DIM_LIN_Location

    :param document: The document to convert.
    :param dwh_engine: The DWH engine to use.
    """
    # Prepare location data
    location_df = conv.location(document)

    # Check if a matching record exists
    query = """
        SELECT id
        FROM DIM_LIN_Location
        WHERE countryLetters = %(countryLetters)s 
        AND countryName = %(countryName)s
        AND city = %(city)s
        AND state = %(state)s
    """
    result = pd.read_sql_query(query, dwh_engine, params=location_df.iloc[0].to_dict())

    if not result.empty:
        # If matching record found, use existing id
        location_id = result.iloc[0]['id']
    else:
        # If no matching record found, insert a new record and use its id
        location_df.to_sql('DIM_LIN_Location', dwh_engine, if_exists='append', index=False)
        location_id = pd.read_sql_query("SELECT LAST_INSERT_ID()", dwh_engine).iloc[0, 0]

    # Return location id
    return location_id


def person(document: dict, location_id: int, origin_id: int, dwh_engine) -> int:
    """
    This function inserts a person into the DWH and returns its ID.

    DWH table: FACT_PRF_Person

    :param document: The document to convert.
    :param location_id: The ID of the location dimension.
    :param origin_id: The ID of the DIM_Origin table from the dwh.
    :param dwh_engine: The DWH engine to use.
    """
    # Prepare person data
    person_df = conv.person(document, location_id, origin_id)

    # Insert person data
    person_df.to_sql('FACT_PRF_Person', dwh_engine, if_exists='append', index=False)
    person_id = pd.read_sql_query("SELECT LAST_INSERT_ID()", dwh_engine).iloc[0, 0]

    # Return person id
    return person_id


def recommendations(document: dict, person_id: int, dwh_engine):
    """
    This function inserts recommendations into the DWH.

    DWH table: FACT_PRF_Recommendation

    :param document: The document to convert.
    :param person_id: The ID of the person in the DWH.
    :param dwh_engine: The DWH engine to use.
    """
    if document.get('recommendations'):
        df_to_add = document.get('recommendations', [])
        data = []

        # Populate list with data
        for rec in df_to_add:
            data.append({
                'idPerson': person_id,
                'recommendationText': rec
            })

        # Create and insert DataFrame
        if data:
            pd.DataFrame(data).to_sql('FACT_PRF_Recommendation', dwh_engine, if_exists='append', index=False)


def people_also_viewed(document: dict, person_id: int, dwh_engine):
    """
    This function inserts people also viewed into the DWH.

    DWH table: FACT_PRF_Related

    :param document: The document to convert.
    :param person_id: The ID of the person in the DWH.
    :param dwh_engine: The DWH engine to use.
    """
    if document.get('people_also_viewed'):
        df_to_add = document.get('people_also_viewed', [])
        data = []

        # Populate list with data
        for ppl in df_to_add:
            data.append({
                'idPerson': person_id,
                'type': 'viewed',
                'name': ppl.get('name'),
                'location': ppl.get('location'),
                'summary': ppl.get('summary')
            })

        # Create and insert DataFrame
        if data:
            pd.DataFrame(data).to_sql('FACT_PRF_Related', dwh_engine, if_exists='append', index=False)


def similarly_named_profiles(document: dict, person_id: int, dwh_engine):
    """
    This function inserts similarly named profiles into the DWH.

    DWH table: FACT_PRF_Related

    :param document: The document to convert.
    :param person_id: The ID of the person in the DWH.
    :param dwh_engine: The DWH engine to use.
    """
    if document.get('similarly_named_profiles'):
        df_to_add = document.get('similarly_named_profiles', [])
        data = []

        # Populate list with data
        for ppl in df_to_add:
            data.append({
                'idPerson': person_id,
                'type': 'similar',
                'name': ppl.get('name'),
                'location': ppl.get('location'),
                'summary': ppl.get('summary')
            })

        # Create and insert DataFrame
        if data:
            pd.DataFrame(data).to_sql('FACT_PRF_Related', dwh_engine, if_exists='append', index=False)


def languages(document: dict, person_id: int, dwh_engine):
    """
    This function inserts languages into the DWH.

    DWH tables: DIM_PRF_Language, REL_PRF_Person_Language

    :param document: The document to convert.
    :param person_id: The ID of the person in the DWH.
    :param dwh_engine: The DWH engine to use.
    """
    if document.get('languages') and len(document.get('languages')) > 0:
        for lang in document.get('languages'):
            # Check if a matching record exists
            query = """
                SELECT id
                FROM DIM_PRF_Language
                WHERE language = %(language)s
            """
            result = pd.read_sql_query(query, dwh_engine, params={'language': lang})

            if not result.empty:
                # If matching record found, use existing id
                lang_id = result.iloc[0]['id']
            else:
                # If no matching record found, insert a new record and use its id
                pd.DataFrame({
                    'language': [lang]
                }).to_sql('DIM_PRF_Language', dwh_engine, if_exists='append', index=False)
                lang_id = pd.read_sql_query("SELECT LAST_INSERT_ID()", dwh_engine).iloc[0, 0]

            # Check if a relationship record already exists
            query = """
                SELECT *
                FROM REL_PRF_Person_Language
                WHERE idPerson = %(idPerson)s
                AND idLanguage = %(idLanguage)s
            """
            result = pd.read_sql_query(query, dwh_engine, params={'idPerson': person_id, 'idLanguage': lang_id})

            # Insert if relationship record does not exist
            if result.empty:
                pd.DataFrame([{
                    'idPerson': person_id,
                    'idLanguage': lang_id
                }]).to_sql('REL_PRF_Person_Language', dwh_engine, if_exists='append', index=False)


def skills(document: dict, person_id: int, dwh_engine):
    """
    This function inserts skills into the DWH.

    DWH tables: DIM_PRF_Trait, REL_PRF_Person_Trait

    :param document: The document to convert.
    :param person_id: The ID of the person in the DWH.
    :param dwh_engine: The DWH engine to use.
    """
    if document.get('skills') and len(document.get('skills')) > 0:
        for skill in document.get('skills'):
            # Check if a matching record exists
            query = """
                SELECT id
                FROM DIM_PRF_Trait
                WHERE type = %(type)s
                AND name = %(name)s
            """
            result = pd.read_sql_query(query, dwh_engine, params={'type': 'skill', 'name': skill})

            if not result.empty:
                # If matching record found, use existing id
                skill_id = result.iloc[0]['id']
            else:
                # If no matching record found, insert a new record and use its id
                pd.DataFrame([{
                    'type': 'skill',
                    'name': skill
                }]).to_sql('DIM_PRF_Trait', dwh_engine, if_exists='append', index=False)
                skill_id = pd.read_sql_query("SELECT LAST_INSERT_ID()", dwh_engine).iloc[0, 0]

            # Check if a relationship record already exists
            query = """
                SELECT *
                FROM REL_PRF_Person_Trait
                WHERE idPerson = %(idPerson)s
                AND idTrait = %(idTrait)s
            """
            result = pd.read_sql_query(query, dwh_engine, params={'idPerson': person_id, 'idTrait': skill_id})

            # Insert if relationship record does not exist
            if result.empty:
                pd.DataFrame([{
                    'idPerson': person_id,
                    'idTrait': skill_id
                }]).to_sql('REL_PRF_Person_Trait', dwh_engine, if_exists='append', index=False)


def interests(document: dict, person_id: int, dwh_engine):
    """
    This function inserts interests into the DWH.

    DWH tables: DIM_PRF_Trait, REL_PRF_Person_Trait

    :param document: The document to convert.
    :param person_id: The ID of the person in the DWH.
    :param dwh_engine: The DWH engine to use.
    """
    if document.get('interests') and len(document.get('interests')) > 0:
        for interest in document.get('interests'):
            # Check if a matching record exists
            query = """
                SELECT id
                FROM DIM_PRF_Trait
                WHERE type = %(type)s
                AND name = %(name)s
            """
            result = pd.read_sql_query(query, dwh_engine, params={'type': 'interest', 'name': interest})

            if not result.empty:
                # If matching record found, use existing id
                interest_id = result.iloc[0]['id']
            else:
                # If no matching record found, insert a new record and use its id
                pd.DataFrame([{
                    'type': 'interest',
                    'name': interest
                }]).to_sql('DIM_PRF_Trait', dwh_engine, if_exists='append', index=False)
                interest_id = pd.read_sql_query("SELECT LAST_INSERT_ID()", dwh_engine).iloc[0, 0]

            # Check if a relationship record already exists
            query = """
                SELECT *
                FROM REL_PRF_Person_Trait
                WHERE idPerson = %(idPerson)s
                AND idTrait = %(idTrait)s
            """
            result = pd.read_sql_query(query, dwh_engine, params={'idPerson': person_id, 'idTrait': interest_id})

            # Insert if relationship record does not exist
            if result.empty:
                pd.DataFrame([{
                    'idPerson': person_id,
                    'idTrait': interest_id
                }]).to_sql('REL_PRF_Person_Trait', dwh_engine, if_exists='append', index=False)


def groups(document: dict, person_id: int, dwh_engine):
    """
    This function inserts groups into the DWH.

    DWH tables: DIM_PRF_Group, REL_PRF_Person_Group

    :param document: The document to convert.
    :param person_id: The ID of the person in the DWH.
    :param dwh_engine: The DWH engine to use.
    """
    if document.get('groups') and len(document.get('groups')) > 0:
        for group in document.get('groups'):
            if group.get('name'):
                # Check if a matching record exists
                query = """
                    SELECT id
                    FROM DIM_PRF_Group
                    WHERE name = %(name)s
                """
                result = pd.read_sql_query(query, dwh_engine, params={'name': group.get('name')})

                if not result.empty:
                    # If matching record found, use existing id
                    group_id = result.iloc[0]['id']
                else:
                    # If no matching record found, insert a new record and use its id
                    pd.DataFrame([{
                        'name': group.get('name')
                    }]).to_sql('DIM_PRF_Group', dwh_engine, if_exists='append', index=False)
                    group_id = pd.read_sql_query("SELECT LAST_INSERT_ID()", dwh_engine).iloc[0, 0]

                # Check if a relationship record already exists
                query = """
                    SELECT *
                    FROM REL_PRF_Person_Group
                    WHERE idPerson = %(idPerson)s
                    AND idGroup = %(idGroup)s
                """
                result = pd.read_sql_query(query, dwh_engine, params={'idPerson': person_id, 'idGroup': group_id})

                # Insert if relationship record does not exist
                if result.empty:
                    pd.DataFrame([{
                        'idPerson': person_id,
                        'idGroup': group_id
                    }]).to_sql('REL_PRF_Person_Group', dwh_engine, if_exists='append', index=False)


def experiences(document: dict, person_id: int, dwh_engine):
    """
    This function inserts experiences into the DWH.

    DWH tables: DIM_PRF_Duration, FACT_PRF_Qualification

    :param document: The document to convert.
    :param person_id: The ID of the person in the DWH.
    :param dwh_engine: The DWH engine to use.
    """
    if document.get('experiences') and len(document.get('experiences')) > 0:
        for experience in document.get('experiences'):
            # Create and fill the duration dimension table
            if experience.get('starts_at') or experience.get('ends_at'):
                duration_df = pd.DataFrame([{
                    'startDate': conv.convert_date(experience.get('starts_at')),
                    'endDate': conv.convert_date(experience.get('ends_at'))
                }])
                # Check if matching records exist
                query = """
                    SELECT id
                    FROM DIM_PRF_Duration
                    WHERE startDate = %(startDate)s
                    AND endDate = %(endDate)s
                """
                result = pd.read_sql_query(query, dwh_engine, params=duration_df.iloc[0].to_dict())

                # If matching records found, use existing id
                if not result.empty:
                    duration_id = result.iloc[0]['id']
                else:
                    # If no matching records found, insert a new record and use its id
                    duration_df.to_sql('DIM_PRF_Duration', dwh_engine, if_exists='append', index=False)
                    duration_id = pd.read_sql_query("SELECT LAST_INSERT_ID()", dwh_engine).iloc[0, 0]
            else:
                duration_id = None

            # Convert experience to FACT_PRF_Qualification table
            experience_df = conv.experience(experience, person_id, duration_id)

            # Insert experience data
            experience_df.to_sql('FACT_PRF_Qualification', dwh_engine, if_exists='append', index=False)


def education(document: dict, person_id: int, dwh_engine):
    """
    This function inserts education into the DWH.

    DWH tables: FACT_PRF_Qualification, DIM_PRF_Duration

    :param document: The document to convert.
    :param person_id: The ID of the person in the DWH.
    :param dwh_engine: The DWH engine to use.
    """
    if document.get('education') and len(document.get('education')) > 0:
        for education in document.get('education'):
            # Create and fill the duration dimension table
            if education.get('starts_at') or education.get('ends_at'):
                duration_df = pd.DataFrame([{
                    'startDate': conv.convert_date(education.get('starts_at')),
                    'endDate': conv.convert_date(education.get('ends_at'))
                }])
                # Check if matching records exist
                query = """
                        SELECT id
                        FROM DIM_PRF_Duration
                        WHERE startDate = %(startDate)s
                        AND endDate = %(endDate)s
                    """
                result = pd.read_sql_query(query, dwh_engine, params=duration_df.iloc[0].to_dict())

                # If matching records found, use existing id
                if not result.empty:
                    duration_id = result.iloc[0]['id']
                else:
                    # If no matching records found, insert a new record and use its id
                    duration_df.to_sql('DIM_PRF_Duration', dwh_engine, if_exists='append', index=False)
                    duration_id = pd.read_sql_query("SELECT LAST_INSERT_ID()", dwh_engine).iloc[0, 0]
            else:
                duration_id = None

            # Convert education to FACT_PRF_Qualification table
            education_df = conv.education(education, person_id, duration_id)

            # Insert education data
            education_df.to_sql('FACT_PRF_Qualification', dwh_engine, if_exists='append', index=False)


def volunteer_work(document: dict, person_id: int, dwh_engine):
    """
    This function inserts volunteer work into the DWH.

    DWH tables: FACT_PRF_Qualification, DIM_PRF_Duration

    :param document: The document to convert.
    :param person_id: The ID of the person in the DWH.
    :param dwh_engine: The DWH engine to use.
    """
    if document.get('volunteer_work') and len(document.get('volunteer_work')) > 0:
        for volunteer in document.get('volunteer_work'):
            # Create and fill the duration dimension table
            if volunteer.get('starts_at') or volunteer.get('ends_at'):
                duration_df = pd.DataFrame([{
                    'startDate': conv.convert_date(volunteer.get('starts_at')),
                    'endDate': conv.convert_date(volunteer.get('ends_at'))
                }])
                # Check if matching records exist
                query = """
                    SELECT id
                    FROM DIM_PRF_Duration
                    WHERE startDate = %(startDate)s
                    AND endDate = %(endDate)s
                """
                result = pd.read_sql_query(query, dwh_engine, params=duration_df.iloc[0].to_dict())

                # If matching records found, use existing id
                if not result.empty:
                    duration_id = result.iloc[0]['id']
                else:
                    # If no matching records found, insert a new record and use its id
                    duration_df.to_sql('DIM_PRF_Duration', dwh_engine, if_exists='append', index=False)
                    duration_id = pd.read_sql_query("SELECT LAST_INSERT_ID()", dwh_engine).iloc[0, 0]
            else:
                duration_id = None

            # Convert volunteer to FACT_PRF_Qualification table
            volunteer_df = conv.volunteer_work(volunteer, person_id, duration_id)

            # Insert volunteer data
            volunteer_df.to_sql('FACT_PRF_Qualification', dwh_engine, if_exists='append', index=False)


def certifications(document: dict, person_id: int, dwh_engine):
    """
    This function inserts certifications into the DWH.

    DWH tables: FACT_PRF_Qualification, DIM_PRF_Duration

    :param document: The document to convert.
    :param person_id: The ID of the person in the DWH.
    :param dwh_engine: The DWH engine to use.
    """
    if document.get('certifications') and len(document.get('certifications')) > 0:
        for certification in document.get('certifications'):
            # Create and fill the duration dimension table
            if certification.get('starts_at') or certification.get('ends_at'):
                duration_df = pd.DataFrame([{
                    'startDate': conv.convert_date(certification.get('starts_at')),
                    'endDate': conv.convert_date(certification.get('ends_at'))
                }])
                # Check if matching records exist
                query = """
                    SELECT id
                    FROM DIM_PRF_Duration
                    WHERE startDate = %(startDate)s
                    AND endDate = %(endDate)s
                """
                result = pd.read_sql_query(query, dwh_engine, params=duration_df.iloc[0].to_dict())

                # If matching records found, use existing id
                if not result.empty:
                    duration_id = result.iloc[0]['id']
                else:
                    # If no matching records found, insert a new record and use its id
                    duration_df.to_sql('DIM_PRF_Duration', dwh_engine, if_exists='append', index=False)
                    duration_id = pd.read_sql_query("SELECT LAST_INSERT_ID()", dwh_engine).iloc[0, 0]
            else:
                duration_id = None

            # Convert certification to FACT_PRF_Qualification table
            certification_df = conv.certification(certification, person_id, duration_id)

            # Insert certification data
            certification_df.to_sql('FACT_PRF_Qualification', dwh_engine, if_exists='append', index=False)


def activities(document: dict, person_id: int, dwh_engine):
    """
    This function inserts activities into the DWH.

    DWH tables: FACT_PRF_Accomplishment

    :param document: The document to convert.
    :param person_id: The ID of the person in the DWH.
    :param dwh_engine: The DWH engine to use.
    """
    if document.get('activities'):
        df_to_add = document.get('activities', [])
        data = []

        # Populate list with data
        for act in df_to_add:
            data.append({
                'idPerson': person_id,
                'type': 'activity',
                'name': act.get('title'),
                'institution': None,
                'date': None,
                'description': act.get('activity_status')
            })

        # Create and insert DataFrame
        if data:
            pd.DataFrame(data).to_sql('FACT_PRF_Accomplishment', dwh_engine, if_exists='append', index=False)


def articles(document: dict, person_id: int, dwh_engine):
    """
    This function inserts articles into the DWH.

    DWH tables: FACT_PRF_Accomplishment

    :param document: The document to convert.
    :param person_id: The ID of the person in the DWH.
    :param dwh_engine: The DWH engine to use.
    """
    if document.get('articles'):
        df_to_add = document.get('articles', [])
        data = []

        # Populate list with data
        for art in df_to_add:
            data.append({
                'idPerson': person_id,
                'type': 'article',
                'name': art.get('title'),
                'institution': art.get('author'),
                'date': conv.convert_date(art.get('published_date')),
                'description': art.get('link')
            })

        # Create and insert DataFrame
        if data:
            pd.DataFrame(data).to_sql('FACT_PRF_Accomplishment', dwh_engine, if_exists='append', index=False)


def accomplishment_organisations(document: dict, person_id: int, dwh_engine):
    """
    This function inserts accomplishment organisations into the DWH.

    DWH tables: FACT_PRF_Accomplishment

    :param document: The document to convert.
    :param person_id: The ID of the person in the DWH.
    :param dwh_engine: The DWH engine to use.
    """
    if document.get('accomplishment_organisations'):
        df_to_add = document.get('accomplishment_organisations', [])
        data = []

        # Populate list with data
        for org in df_to_add:
            data.append({
                'idPerson': person_id,
                'type': 'organisation',
                'name': org.get('title'),
                'institution': org.get('org_name'),
                'date': conv.convert_date(org.get('starts_at')),
                'description': org.get('description')
            })

        # Create and insert DataFrame
        if data:
            pd.DataFrame(data).to_sql('FACT_PRF_Accomplishment', dwh_engine, if_exists='append', index=False)


def accomplishment_publications(document: dict, person_id: int, dwh_engine):
    """
    This function inserts accomplishment publications into the DWH.

    DWH tables: FACT_PRF_Accomplishment

    :param document: The document to convert.
    :param person_id: The ID of the person in the DWH.
    :param dwh_engine: The DWH engine to use.
    """
    if document.get('accomplishment_publications'):
        df_to_add = document.get('accomplishment_publications', [])
        data = []

        # Populate list with data
        for pub in df_to_add:
            data.append({
                'idPerson': person_id,
                'type': 'publication',
                'name': pub.get('name'),
                'institution': pub.get('publisher'),
                'date': conv.convert_date(pub.get('published_on')),
                'description': pub.get('description')
            })

        # Create and insert DataFrame
        if data:
            pd.DataFrame(data).to_sql('FACT_PRF_Accomplishment', dwh_engine, if_exists='append', index=False)


def accomplishment_honors_awards(document: dict, person_id: int, dwh_engine):
    """
    This function inserts accomplishment honor awards into the DWH.

    DWH tables: FACT_PRF_Accomplishment

    :param document: The document to convert.
    :param person_id: The ID of the person in the DWH.
    :param dwh_engine: The DWH engine to use.
    """
    if document.get('accomplishment_honors_awards'):
        df_to_add = document.get('accomplishment_honors_awards', [])
        data = []

        # Populate list with data
        for hon in df_to_add:
            data.append({
                'idPerson': person_id,
                'type': 'honor',
                'name': hon.get('title'),
                'institution': hon.get('issuer'),
                'date': conv.convert_date(hon.get('issued_on')),
                'description': hon.get('description')
            })

        # Create and insert DataFrame
        if data:
            pd.DataFrame(data).to_sql('FACT_PRF_Accomplishment', dwh_engine, if_exists='append', index=False)


def accomplishment_patents(document: dict, person_id: int, dwh_engine):
    """
    This function inserts accomplishment patents into the DWH.

    DWH tables: FACT_PRF_Accomplishment

    :param document: The document to convert.
    :param person_id: The ID of the person in the DWH.
    :param dwh_engine: The DWH engine to use.
    """
    if document.get('accomplishment_patents'):
        df_to_add = document.get('accomplishment_patents', [])
        data = []

        # Populate list with data
        for pat in df_to_add:
            # Get the variables
            application_number = pat.get('application_number', None)
            patent_number = pat.get('patent_number', None)
            patent_description = pat.get('description', None)

            # Use match case to determine the description
            match (application_number, patent_number, patent_description):
                case (None, None, None):
                    # If all are None, set the combined description to None
                    comb_description = None
                case (None, _, None):
                    # If only patent_number is available, use it as the description
                    comb_description = patent_number
                case (None, _, _):
                    # If patent_number and description are available, combine them
                    comb_description = f"{patent_number} | {patent_description}"
                case (_, None, None):
                    # If only application_number is available, use it as the description
                    comb_description = application_number
                case (_, None, _):
                    # If application_number and description are available, combine them
                    comb_description = f"{application_number} | {patent_description}"
                case (_, _, None):
                    # If application_number and patent_number are available, combine them
                    comb_description = f"{application_number} | {patent_number}"
                case _:
                    # If all are available, combine all three
                    comb_description = f"{application_number} | {patent_number} | {patent_description}"

            data.append({
                'idPerson': person_id,
                'type': 'patent',
                'name': pat.get('title'),
                'institution': pat.get('issuer'),
                'date': conv.convert_date(pat.get('issued_on')),
                'description': comb_description
            })

        # Create and insert DataFrame
        if data:
            pd.DataFrame(data).to_sql('FACT_PRF_Accomplishment', dwh_engine, if_exists='append', index=False)


def accomplishment_test_scores(document: dict, person_id: int, dwh_engine):
    """
    This function inserts accomplishment test scores into the DWH.

    DWH tables: FACT_PRF_Accomplishment

    :param document: The document to convert.
    :param person_id: The ID of the person in the DWH.
    :param dwh_engine: The DWH engine to use.
    """
    if document.get('accomplishment_test_scores'):
        df_to_add = document.get('accomplishment_test_scores', [])
        data = []

        # Populate list with data
        for tst in df_to_add:
            data.append({
                'idPerson': person_id,
                'type': 'test',
                'name': tst.get('name'),
                'institution': tst.get('score'),
                'date': conv.convert_date(tst.get('date_on')),
                'description': tst.get('description')
            })

        # Create and insert DataFrame
        if data:
            pd.DataFrame(data).to_sql('FACT_PRF_Accomplishment', dwh_engine, if_exists='append', index=False)


def accomplishment_courses(document: dict, person_id: int, dwh_engine):
    """
    This function inserts accomplishment courses into the DWH.

    DWH tables: FACT_PRF_Accomplishment

    :param document: The document to convert.
    :param person_id: The ID of the person in the DWH.
    :param dwh_engine: The DWH engine to use.
    """
    if document.get('accomplishment_courses'):
        df_to_add = document.get('accomplishment_courses', [])
        data = []

        # Populate list with data
        for crs in df_to_add:
            data.append({
                'idPerson': person_id,
                'type': 'course',
                'name': crs.get('name'),
                'institution': crs.get('number'),
                'date': None,
                'description': None
            })

        # Create and insert DataFrame
        if data:
            pd.DataFrame(data).to_sql('FACT_PRF_Accomplishment', dwh_engine, if_exists='append', index=False)


def accomplishment_projects(document: dict, person_id: int, dwh_engine):
    """
    This function inserts accomplishment projects into the DWH.

    DWH tables: FACT_PRF_Qualification

    :param document: The document to convert.
    :param person_id: The ID of the person in the DWH.
    :param dwh_engine: The DWH engine to use.
    """
    if document.get('accomplishment_projects') and len(document.get('accomplishment_projects')) > 0:
        for project in document.get('accomplishment_projects'):
            # Create and fill the duration dimension table
            if project.get('starts_at') or project.get('ends_at'):
                duration_df = pd.DataFrame([{
                    'startDate': conv.convert_date(project.get('starts_at')),
                    'endDate': conv.convert_date(project.get('ends_at'))
                }])
                # Check if matching records exist
                query = """
                    SELECT id
                    FROM DIM_PRF_Duration
                    WHERE startDate = %(startDate)s
                    AND endDate = %(endDate)s
                """
                result = pd.read_sql_query(query, dwh_engine, params=duration_df.iloc[0].to_dict())

                # If matching records found, use existing id
                if not result.empty:
                    duration_id = result.iloc[0]['id']
                else:
                    # If no matching records found, insert a new record and use its id
                    duration_df.to_sql('DIM_PRF_Duration', dwh_engine, if_exists='append', index=False)
                    duration_id = pd.read_sql_query("SELECT LAST_INSERT_ID()", dwh_engine).iloc[0, 0]
            else:
                duration_id = None

            # Convert accomplishment_projects to FACT_PRF_Qualification table
            project_df = conv.accomplishment_projects(project, person_id, duration_id)

            # Insert certification data
            project_df.to_sql('FACT_PRF_Qualification', dwh_engine, if_exists='append', index=False)
