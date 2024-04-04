import json
def generate_monogo_pipeline(template_file_path, iterable_list):
    
    """ Tạo template để đem vào aggregation pipepline

    Args:
        template: json format
        iterable_list: 1d array of parameters for template
    
    Return:
        pipeline_templates: 1d array of json

    """
    with open(template_file_path, 'r') as f:
        template = json.load(f)
    
    pipline_list = []
    for value in iterable_list:
        # Generate pipeline using the template and current value
        pipeline = template.copy()  # Create a copy of the template dictionary
        pipeline[0]["$match"]["segm"] = value  # Update the value of the degree field
        pipline_list.append(pipeline)

    return pipline_list

