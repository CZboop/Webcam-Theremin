s.boot;

(
OSCdef.new(
	\theremin,
	{
		arg msg, time, addr, port;
		[msg[1], msg[2]].postln;

	},'/theremin'
);
SynthDef( \sineFrom, { | amp = 0.01, freq = 333, trig = 1 |
    var env, sig;
    env = EnvGen.kr( Env.asr( 0.001, 0.9, 0.001 ), trig, doneAction: 0 );
    sig = LFTri.ar( [ freq, freq * 0.999 ], 0.0, amp ) * env;
    Out.ar( [ 0 ], sig * 0.6 );
}).add;

t = Synth( \sineFrom, {SinOsc.ar(freq: 300, mul: 0.5)});

x = OSCFunc( { | msg, time, addr, port |
    var therFreq;
	var therMul;

    therFreq = msg[1];
	therMul = msg[2];
	t.set( \freq, LinLin.kr(therFreq, 0, 1, 100,1000), \mul, LinLin.kr(therMul, 0, 1, 0,2) );
	// t.set( \mul, therMul );
}, "/theremin" );
)