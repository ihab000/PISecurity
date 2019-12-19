var Blynk = require("blynk-library");

var AUTH = 'tCyL_uIFb2im-MnKC5FjFwMaP1k8ekTf';

var blynk = new Blynk.Blynk(AUTH);

var v1 = new blynk.VirtualPin(1);

v1.on('write', function(param) {
  if (param == 1) {
	runScript() };
});


function runScript() {

const { spawn } = require('child_process')

const logOutput = (name) => (data) => console.log(`[${name}] ${data.toString()}`)

function run() {
  const process = spawn('python3', ['./PISecurityv2.py']);


  process.stdout.on(
    'data',
    logOutput('stdout')
  );

  process.stderr.on(
    'data',
    logOutput('stderr')
  );

  process.stdin.on(
    'data',
    logOutput('stdin')
  );
}

(() => {
  try {
    run()
    // process.exit(0)
  } catch (e) {
    console.error(e.stack);
    process.exit(1);
  }
})();
}

