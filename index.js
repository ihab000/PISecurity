var Blynk = require("blynk-library");

var AUTH = 'tCyL_uIFb2im-MnKC5FjFwMaP1k8ekTf';

var blynk = new Blynk.Blynk(AUTH);

var v1 = new blynk.VirtualPin(1);

const shell = require('shelljs')

v1.on('write', function(param) {
  if (param == 1) {
	runScript() }
	if (param == 0) {
		shell.exec('/home/pi/Assignment2/stop.sh')	};
});


function runScript() {

const { spawn } = require('child_process')

const logOutput = (name) => (data) => console.log(`[${name}] ${data.toString()}`)

function run() {
  const process = spawn('python3', ['/home/pi/Assignment2/PISecurityv4.py']);


  process.stdout.on(
    'data',
    logOutput('stdout')
  );

  process.stderr.on(
    'data',
    logOutput('stderr')
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

