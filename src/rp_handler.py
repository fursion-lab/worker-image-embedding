import base64
import tempfile

from rp_schema import INPUT_VALIDATIONS
from runpod.serverless.utils import download_files_from_urls, rp_cleanup, rp_debugger
from runpod.serverless.utils.rp_validator import validate
import runpod
import predict


def base64_to_tempfile(base64_file: str) -> str:
    '''
    Convert base64 file to tempfile.

    Parameters:
    base64_file (str): Base64 file

    Returns:
    str: Path to tempfile
    '''
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as temp_file:
        temp_file.write(base64.b64decode(base64_file))

    return temp_file.name


@rp_debugger.FunctionTimer
def run_encode_job(job):
    '''
    Run inference on the model.

    Parameters:
    job (dict): Input job containing the model parameters

    Returns:
    dict: The result of the prediction
    '''
    job_input = job['input']

    with rp_debugger.LineTimer('validation_step'):
        input_validation = validate(job_input, INPUT_VALIDATIONS)

        if 'errors' in input_validation:
            return {"error": input_validation['errors']}
        job_input = input_validation['validated_input']

    if not job_input.get('image', False) and not job_input.get('image_base64', False):
        return {'error': 'Must provide either image or image_base64'}

    if job_input.get('image', False) and job_input.get('image_base64', False):
        return {'error': 'Must provide either image or image_base64, not both'}

    if job_input.get('image', False):
        with rp_debugger.LineTimer('download_step'):
            image_input = download_files_from_urls(job['id'], [job_input['image']])[0]

    if job_input.get('image_base64', False):
        image_input = base64_to_tempfile(job_input['audio_base64'])

    with rp_debugger.LineTimer('embed_step'):
        embedding = predict.embed_image(image_input)

    with rp_debugger.LineTimer('cleanup_step'):
        rp_cleanup.clean(['input_objects'])

    return {'embedding': embedding}


runpod.serverless.start({"handler": run_encode_job})
