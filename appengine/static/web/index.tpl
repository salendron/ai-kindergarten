<!DOCTYPE html>
<html>

<head>
  <meta charset="utf-8">
  <title>AI - Kindergarten</title>
  <meta name="author" content="Bruno Hautzenberger">
  <meta name="description" content="An experiment on Tensorflow models learning to play simple games.">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link href="css/style.css" rel="stylesheet">
  <link href="css/tictactoe.css" rel="stylesheet">
</head>

<body>
    <div id="header">
        AI Kindergarten
    </div>

    <div id="main">
        <div id="main-content">
            % if content == 'tictactoe':
              % include('tictactoe/index.tpl')
            % end
        </div>
    </div>

    <div id="footer">
        This is a machine learning experiment by Bruno Hautzenberger. You can contact me via <a href="mailto:bruno@xamoom.com">email</a> or find me on <a href="https://twitter.com/salendron">Twitter.</a>
        This site does not use any 3rd party tracking services like Google Analytics or anything like that. There are also no like or share buttons. If you want to share this, just copy the link and post it where ever you want to.
        The only thing that is saved are the games you played, which basically is just a bunch of numbers from 0 to 8 (all 9 fields).
    </div>
</body>

</html>