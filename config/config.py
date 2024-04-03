# import joblib
import json
# MODEL_PATH = './SVD.pkl'

# SAVED_MODEL = joblib.load(MODEL_PATH)

def generate_monogo_template(template_file_path, iterable_list):
    
    """ Tạo template để đem vào aggregation pipepline

    Args:
        template: json format
        iterable_list: 1d array of parameters for template
    
    Return:
        pipeline_templates: 1d array of json

    """
    with open(template_file_path, 'r') as f:
        template = json.load(f)
 
    templates_list = []
    for value in iterable_list:
        # Generate pipeline using the template and current value
        pipeline = template[0].copy()  # Create a copy of the template dictionary
        pipeline["$match"]["$degree"] = value  # Update the value of the degree field
        templates_list.append(pipeline)

    return templates_list

value = generate_monogo_template(r"D:\DuyTan_algorithm_demo\config\result_template.json",
                         [1,2,3])

print(value)