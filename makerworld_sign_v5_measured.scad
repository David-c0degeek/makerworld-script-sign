// MakerWorld OpenSCAD: Great Vibes three-line sign, v5 (mesh-measured repairs)
// Calibrated from the clean Great Vibes MakerWorld screenshot.
// This arrangement is for THESE EXACT THREE LINES ONLY.
// A minimalist cutout: short ligatures + two near-touching line joints.

fontName = "Great Vibes";
fontSize = 24;
letterGrow = 0.35;
letterHeight = 3.6;
stitchHeight = 3.0;    // Raised text covers stitches where they overlap.
modelScale = 0.80;    // Check overall X/Y dimensions in MakerWorld.
printAngle = 0;       // Rotate in Bambu Studio if preferred.
extraBracing = false; // True = 2 extra short structural joints.

line1 = "May your stress";
line2 = "turn into a fart";
line3 = "and leave your body";

// New layout brings the natural descenders/ascenders close together.
// Changing these requires adjusting the calibrated stitch coordinates.
pos1 = [-10, 30];
pos2 = [ 14,  0];
pos3 = [-5.5,-29];
$fn = 24;

module letters() {
    translate(pos1) offset(r=letterGrow)
        text(line1,font=fontName,size=fontSize,halign="center",valign="baseline");
    translate(pos2) offset(r=letterGrow)
        text(line2,font=fontName,size=fontSize,halign="center",valign="baseline");
    translate(pos3) offset(r=letterGrow)
        text(line3,font=fontName,size=fontSize,halign="center",valign="baseline");
}

function bez(a,b,c,d,t) =
    pow(1-t,3)*a + 3*pow(1-t,2)*t*b +
    3*(1-t)*t*t*c + pow(t,3)*d;

// Each stitch terminates inside the two existing letter strokes.
// Thin rounded cubic strokes look like joining ligatures, not bars.
module stitch(a,d,w=1.15,bend=0,steps=10) {
    v=d-a;
    n=[-v[1],v[0]]/norm(v);
    b=a+v*0.33+n*bend;
    c=a+v*0.67+n*bend;
    for (i=[0:steps-1])
        hull() {
            translate(bez(a,b,c,d,i/steps)) circle(d=w);
            translate(bez(a,b,c,d,(i+1)/steps)) circle(d=w);
        }
}

module joins() {
    // Original small May letter join (reinforced by the measured weld below)
    stitch([-55.77,38.07], [-52.91,36.64], 1.40, 0.00);
    // May to your
    stitch([-28.23,36.54], [-21.96,33.65], 1.45, 0.25);
    // your to stress
    stitch([23.48,36.19], [27.84,34.00], 1.45, 0.15);
    // May y to turn
    stitch([-45.62,20.25], [-47.21,17.86], 2.30, 0.00);
    // turn to into
    stitch([-15.08,5.80], [-9.45,4.77], 1.45, 0.15);
    // i dot
    stitch([-5.84,11.34], [-5.10,14.32], 1.25, 0.00);
    // into to a
    stitch([26.43,6.17], [32.06,5.15], 1.45, -0.15);
    // a to fart
    stitch([43.83,4.83], [47.86,3.10], 1.45, -0.10);
    // f to b
    stitch([49.47,-9.14], [50.53,-11.24], 2.30, 0.00);
    // b to ody
    stitch([52.83,-22.64], [55.09,-22.64], 1.40, 0.00);
    // your to body
    stitch([38.14,-23.58], [43.75,-25.10], 1.45, 0.15);
    // leave to your
    stitch([-12.76,-23.08], [-7.24,-25.60], 1.45, -0.15);
    // Original small and-to-leave stitch (reinforced below)
    stitch([-65.27,-22.51], [-59.63,-23.53], 1.45, 0.15);
    // EXACT WELDS FROM THE EXPORTED V4 STL (UNSCALED SCAD COORDINATES)
    // Existing stitches almost, but do not quite, meet these two words.
    // 2.875 mm here = 2.3 mm on the final 0.80-scaled model.
    // These are short, rounded, low-profile seams; not full-width rails.
    // May -> your: measured exported mesh gap was 0.037 mm.
    stitch([-54.50, 37.25],[-51.00, 35.50],2.875,0,14);
    // and -> leave: measured exported mesh gap was 0.431 mm.
    stitch([-61.25,-23.00],[-56.75,-24.50],2.875,0,14);

    if (extraBracing) {
    // upper backup
    stitch([-27.92,20.65], [-31.32,14.82], 1.50, -0.70);
    // lower backup
    stitch([-52.08,0.75], [-52.08,-8.30], 1.50, 0.60);
    }
}

rotate([0,0,printAngle])
    scale([modelScale,modelScale,1])
        union() {
            linear_extrude(height=stitchHeight) joins();
            linear_extrude(height=letterHeight) letters();
        }
