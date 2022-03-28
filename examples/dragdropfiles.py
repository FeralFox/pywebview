import webview

"""
This example demonstrates how to expose Python functions to the Javascript domain.
"""


def expose(window):
    pass


html = '''<html><head></head>
<script type="text/javascript">
let _DROPPED_PATHS;
function mousedown(event) {
    if (!_DROPPED_PATHS) {return}
    // Was not sure how to post it, 
    chrome.webview.postMessage(["dragfile", {files: _DROPPED_PATHS}, 42])
}

async function drop(event) {
    file_names = []
    for (let file of event.dataTransfer.files) {
        file_names.push(file.name)    
    }
    let response = await pywebview.api.dropped_files(file_names)
    _DROPPED_PATHS = response
    document.getElementById('box').innerText = `Drag me now!\n\n${_DROPPED_PATHS.join('\\n')}`
}

function dragover(event) {
    event.preventDefault()
}

</script>
<body>
<div id="box" style="width: 100%; height: 100%; background-color: lightGrey" 
     onmousedown="mousedown(event)" 
     ondragover="dragover(event)" 
     ondrop="drop(event)">Drop files on me!</div>
</body>
</html>'''

if __name__ == '__main__':
    window = webview.create_window('Drag files example', html=html)

    def dropped_files(files):
        base_path = window.get_drop_path()
        files = [base_path / file for file in files]
        print(f'Dropped files: {files}')
        return [f.as_uri() for f in files]


    window.expose(dropped_files)

    webview.start(expose, window, debug=True)
