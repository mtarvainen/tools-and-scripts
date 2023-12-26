#!/usr/bin/env python3
"""
Traverse current working directory tree and convert found INPUT_EXTENSION files to OUTPUT_EXTENSION files.

Requirements: ffmpeg [apt install ffmpeg | yum install ffmpeg | brew install ffmpeg]
"""
import argparse
import os
import concurrent.futures
import pathlib
import shutil
import subprocess
import tqdm

__author__ = "Mikko Tarvainen"
__version__ = "0.2.1"
__license__ = "MIT"

def get_directories(directory):
    return [path for path in pathlib.Path(directory).glob('**/') if not any(part.startswith('.') for part in path.parts)]

def get_files(directory, extension):
    return [file for file in pathlib.Path(directory).glob('*') if file.suffix.replace('.','') == extension]

def fetch_payload(filelist, io):
    payload = []
    for input_file in filelist:
        output_path = os.path.join(os.path.dirname(input_file), io['output_extension'])
        output_file = os.path.join(output_path, os.path.basename(input_file).replace(io['input_extension'], io['output_extension']))
        input_file = str(input_file)
        task = {
            'processed': False,
            'output_file': output_file,
            'input_file': input_file,
            'command': ['ffmpeg', '-y', '-loglevel', 'error', '-i', input_file]
        }
        task['command'].extend(_get_params_by_id(io))
        task['command'].extend([output_file])
        payload.append(task)
    return payload

def _get_params_by_id(io):
    params = []
    if io['input_extension'] == 'flac' and io['output_extension'] == 'mp3':
        params = ['-ab', '320k', '-map_metadata', '0', '-id3v2_version', '3']
    if io['output_extension'] in ['sub', 'srt']:
        params = ['-map', f"0:s:{ io['subtitle_stream_id'] }", '-c:s', 'copy']
    if io['output_extension'] in ['mp4']:
        params = ['-vcodec', 'libx265', '-x265-params', 'lossless=1', '-preset', 'fast']
        if io['crf_value'] > 0:
            params = ['-vcodec', 'libx265', '-crf', f"{ io['crf_value'] }", '-preset', 'fast']
    # if input_extension == 'avi' and output_extension == 'mp4':
    #     pass
    return params

def process_file(task):
    if os.path.exists(task['output_file']) == False:
        process = subprocess.Popen(task['command'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        stdout, stderr = process.communicate()
        returncode = process.wait()
        if returncode == 0:
            task['processed'] = True
        task['stdout'] = stdout
        task['stderr'] = stderr
        task['pid'] = os.getpid()
    return task

def main(args):
    dirlist = get_directories(os.getcwd())
    io = {
        'input_extension': args.input_extension, 
        'output_extension': args.output_extension, 
        'subtitle_stream_id': args.subtitle_stream_id,
        'crf_value': args.crf_value
    }
    tasks = []
    for dir_item in dirlist:
        output_path = os.path.join(dir_item, args.output_extension)
        filelist = get_files(dir_item, io['input_extension'])
        payload = fetch_payload(filelist, io)
        if payload:
            if args.force and os.path.exists(output_path):
                shutil.rmtree(output_path)
            pathlib.Path(output_path).mkdir(exist_ok=True)
        tasks.extend(payload)
    with tqdm.tqdm(total=len(tasks), desc='Processing...') as pbar:
        with concurrent.futures.ProcessPoolExecutor() as executor:
            processes = {executor.submit(process_file, task): task for task in tasks}
            for task in concurrent.futures.as_completed(processes):
                data = task.result()
                if not data['processed']:
                    print(data)
                pbar.update(1)
                #print(f"[ppid={ os.getpid() }, pid={ data['pid'] }]: { data['output_file'] }")
    if args.stty_sane:
        os.system('stty sane')
    return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input-extension", dest="input_extension", help="Extension of input files eg. flac", action="store", required=True)
    parser.add_argument("-o", "--output-extension", dest="output_extension", help="Extension of output files eg. mp3", action="store", required=True)
    parser.add_argument("-s", "--subtitle-stream-id", dest="subtitle_stream_id", default=0, help="Subtitle position in media stream.", action="store", required=False)
    parser.add_argument('-c', "--crf-value", type=int, dest="crf_value", default=0, help="H.265 video codec CRF value for MP4 media file. Lower value leads larger file size.", action="store", required=False, choices=range(16,30))
    parser.add_argument("-f", "--force", dest="force", help="Regenerate new version and overwrite old", action="store_true", default=False)
    parser.add_argument("--stty-sane", dest="stty_sane", help="Ensure optimal terminal line settings", action="store_true", default=True)
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s (version {version})".format(version=__version__))
    args = parser.parse_args()
    main(args)
