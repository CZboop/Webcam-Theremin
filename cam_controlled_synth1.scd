s.boot;

(
OSCdef.new(
	\theremin,
	{
		arg msg, time, addr, port;
		[msg[1], msg[2], msg[3]].postln;

	},'/theremin'
);
SynthDef( \sineFrom, { | amp = 1, freq = 333, trig = 5 |
    var env, sig;
    env = EnvGen.kr( Env.asr( 110.1, 150.9, 10.1 ), trig, doneAction: 0 );
    sig = LFTri.ar( [ freq, freq * 0.299 ], 3.0, amp ) * env;
    Out.ar( [ 0 ], sig * 2.6 );
}).add;

t = Synth( \sineFrom, {SinOsc.ar(freq: 300, phase: 1.0, mul: 0.5 )});

x = OSCFunc( { | msg, time, addr, port |
    var therFreq;
	var therMul;
	var therDist;

    therFreq = msg[1];
	therMul = msg[2];
	therDist = msg[3];
	t.set( \freq, LinLin.kr(therFreq, 0, 1, 100,1000), \mul, LinLin.kr(therMul, 0, 1, 0,2), \amp, therDist );
}, "/theremin" );
)