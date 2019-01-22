<script language="JavaScript">

    function play(move){
        document.getElementById("overlay").style.display = "block";
        document.getElementById("move").value = move;
        document.getElementById("game").submit();
    }

    function new_game(){
        document.getElementById("overlay").style.display = "block";
        window.location.href = "/";
    }

</script>

<div id="overlay">
<div id="overlaytext">Loading...</div>
</div>

<div id="tictactoe-header">
    <h1>TicTacToe</h1>
    <p>This is a machine learning experiment using <a href="https://www.tensorflow.org/">Tensorflow</a> and
        <a href="https://cloud.google.com/ml-engine/">Google Cloud ML-Engine</a>.</p>
    <p>What you do here is playing TicTacToe against a Tensorflow model, that is only trained on games it
    plays against humans. We call it <b>Bob</b>.</p>
</div>

% if winner != -1 and winner != 2:
<div class="tictactoe-winner">
    <h2>{{ winner_name }} won!</h2>
    <a href="#" onclick="new_game()">Play Again</a>
</div>
% end

% if winner == 2:
<div class="tictactoe-winner">
    <h2>Game ended in a tie.</h2>
    <a href="#" onclick="new_game()">Play Again</a>
</div>
% end

<div id="tictactoe-players">
    <p>
        <img src="img/x.png" class="tictactoe-tile-icon" /> {{ player0 }} &nbsp;&nbsp;&nbsp;
        <img src="img/o.png" class="tictactoe-tile-icon" /> {{ player1 }}
    </p>
</div>

<form id="game" name="game" action="/" method="POST">
    <input type="hidden" name="game_token" value="{{ token }}">
    <input type="hidden" name="move" id="move" value="-1">
    <div id="tictactoe-field" class="divTable" >
        <div class="divTableBody">
            <div class="divTableRow">
                <div class="divTableCell">
                    % if field0 == -1 and winner == -1:
                      <a href="#" onclick="play(0);"><img src="img/set.png" class="tictactoe-tile" /></a>
                    % end
                    % if field0 == 0:
                      <img src="img/x.png" class="tictactoe-tile" />
                    % end
                    % if field0 == 1:
                      <img src="img/o.png" class="tictactoe-tile" />
                    % end
                </div>
                <div class="divTableCell">
                     % if field1 == -1 and winner == -1:
                      <a href="#" onclick="play(1);"><img src="img/set.png" class="tictactoe-tile" /></a>
                    % end
                    % if field1 == 0:
                      <img src="img/x.png" class="tictactoe-tile" />
                    % end
                    % if field1 == 1:
                      <img src="img/o.png" class="tictactoe-tile" />
                    % end
                </div>
                <div class="divTableCell">
                     % if field2 == -1 and winner == -1:
                      <a href="#" onclick="play(2);"><img src="img/set.png" class="tictactoe-tile" /></a>
                    % end
                    % if field2 == 0:
                      <img src="img/x.png" class="tictactoe-tile" />
                    % end
                    % if field2 == 1:
                      <img src="img/o.png" class="tictactoe-tile" />
                    % end
                </div>
            </div>
            <div class="divTableRow">
                <div class="divTableCell">
                    % if field3 == -1 and winner == -1:
                      <a href="#" onclick="play(3);"><img src="img/set.png" class="tictactoe-tile" /></a>
                    % end
                    % if field3 == 0:
                      <img src="img/x.png" class="tictactoe-tile" />
                    % end
                    % if field3 == 1:
                      <img src="img/o.png" class="tictactoe-tile" />
                    % end
                </div>
                <div class="divTableCell">
                     % if field4 == -1 and winner == -1:
                      <a href="#" onclick="play(4);"><img src="img/set.png" class="tictactoe-tile" /></a>
                    % end
                    % if field4 == 0:
                      <img src="img/x.png" class="tictactoe-tile" />
                    % end
                    % if field4 == 1:
                      <img src="img/o.png" class="tictactoe-tile" />
                    % end
                </div>
                <div class="divTableCell">
                    % if field5 == -1 and winner == -1:
                      <a href="#" onclick="play(5);"><img src="img/set.png" class="tictactoe-tile" /></a>
                    % end
                    % if field5 == 0:
                      <img src="img/x.png" class="tictactoe-tile" />
                    % end
                    % if field5 == 1:
                      <img src="img/o.png" class="tictactoe-tile" />
                    % end
                </div>
            </div>
            <div class="divTableRow">
                <div class="divTableCell">
                    % if field6 == -1 and winner == -1:
                      <a href="#" onclick="play(6);"><img src="img/set.png" class="tictactoe-tile" /></a>
                    % end
                    % if field6 == 0:
                      <img src="img/x.png" class="tictactoe-tile" />
                    % end
                    % if field6 == 1:
                      <img src="img/o.png" class="tictactoe-tile" />
                    % end
                </div>
                <div class="divTableCell">
                    % if field7 == -1 and winner == -1:
                      <a href="#" onclick="play(7);"><img src="img/set.png" class="tictactoe-tile" /></a>
                    % end
                    % if field7 == 0:
                      <img src="img/x.png" class="tictactoe-tile" />
                    % end
                    % if field7 == 1:
                      <img src="img/o.png" class="tictactoe-tile" />
                    % end
                </div>
                <div class="divTableCell">
                    % if field8 == -1 and winner == -1:
                      <a href="#" onclick="play(8);"><img src="img/set.png" class="tictactoe-tile" /></a>
                    % end
                    % if field8 == 0:
                      <img src="img/x.png" class="tictactoe-tile" />
                    % end
                    % if field8 == 1:
                      <img src="img/o.png" class="tictactoe-tile" />
                    % end
                </div>
            </div>
        </div>
    </div>
</form>

<div id="tictactoe-instructions">
    <p>Just klick on a free field to play your move.</p>
</div>

<div id="tictactoe-footer">
    <p>Every game you play here is recorded and used to train Bob. Since training happens on Google Cloud ML-Engine
    it is done periodically, every few hours. So play some games and come back a few hours later to see how Bob improved.</p>
    <p>Remember, it can only get as good as all people playing against it are. Another thing to keep in mind is,
    that TicTacToe is a game in which player 1 can't loose if he plays perfectly. So if you play a tie against Bob,
    that's actually an awesome outcome for the machine.</p>
</div>

<div id="tictactoe-stats" style="display:none;">
    <p>So far Bob has played <b>{{ stats_h + stats_m + stats_t }}</b> matches. He <b>lost {{ stats_h }}</b> and <b>won {{ stats_m }}</b> of them. There were <b>{{ stats_t }} ties</b>.
    He was last trained on {{ last_train }} UTC.
</div>