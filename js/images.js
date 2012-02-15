//$.getJSON('cgi-bin/GetStoredResult.py', {'id':getParameterByName('permalink')}, populateFromStoredResult);
//http://api.bing.net/json.aspx?AppId= YOUR_APPID &Version=2.2&Market=en-US&Query=testign&Sources=web+spell&Web.Count= 1
function getImageForCeleb(name){
    // console.log(name);
    $.get('http://api.bing.net/json.aspx?callback=?',
        {
            AppId : '1BA29F3AE82559D9A6460AF4C976D71E2F033365',
            Query : 'help',
            Sources : 'Image'
        },
            imageResponseHandler,
        'json'
        );
}

function imageResponseHandler(data){
    // console.log('rxed img')
        // console.log(
            data
        );
}
