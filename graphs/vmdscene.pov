// 
// Molecular graphics export from VMD 1.9.3
// http://www.ks.uiuc.edu/Research/vmd/
// Requires POV-Ray 3.5 or later
// 
// POV 3.x input script : vmdscene.pov 
// try povray +W1510 +H743 -Ivmdscene.pov -Ovmdscene.pov.tga +P +X +A +FT +C
#if (version < 3.5) 
#error "VMD POV3DisplayDevice has been compiled for POV-Ray 3.5 or above.\nPlease upgrade POV-Ray or recompile VMD."
#end 
#declare VMD_clip_on=array[3] {0, 0, 0};
#declare VMD_clip=array[3];
#declare VMD_scaledclip=array[3];
#declare VMD_line_width=0.0020;
#macro VMDC ( C1 )
  texture { pigment { rgbt C1 }}
#end
#macro VMD_point (P1, R1, C1)
  #local T = texture { finish { ambient 1.0 diffuse 0.0 phong 0.0 specular 0.0 } pigment { C1 } }
  #if(VMD_clip_on[2])
  intersection {
    sphere {P1, R1 texture {T} #if(VMD_clip_on[1]) clipped_by {VMD_clip[1]} #end no_shadow}
    VMD_clip[2]
  }
  #else
  sphere {P1, R1 texture {T} #if(VMD_clip_on[1]) clipped_by {VMD_clip[1]} #end no_shadow}
  #end
#end
#macro VMD_line (P1, P2, C1)
  #local T = texture { finish { ambient 1.0 diffuse 0.0 phong 0.0 specular 0.0 } pigment { C1 } }
  #if(VMD_clip_on[2])
  intersection {
    cylinder {P1, P2, VMD_line_width texture {T} #if(VMD_clip_on[1]) clipped_by {VMD_clip[1]} #end no_shadow}
    VMD_clip[2]
  }
  #else
  cylinder {P1, P2, VMD_line_width texture {T} #if(VMD_clip_on[1]) clipped_by {VMD_clip[1]} #end no_shadow}
  #end
#end
#macro VMD_sphere (P1, R1, C1)
  #local T = texture { pigment { C1 } }
  #if(VMD_clip_on[2])
  intersection {
    sphere {P1, R1 texture {T} #if(VMD_clip_on[1]) clipped_by {VMD_clip[1]} #end no_shadow}
    VMD_clip[2]
  }
  #else
  sphere {P1, R1 texture {T} #if(VMD_clip_on[1]) clipped_by {VMD_clip[1]} #end no_shadow}
  #end
#end
#macro VMD_cylinder (P1, P2, R1, C1, O1)
  #local T = texture { pigment { C1 } }
  #if(VMD_clip_on[2])
  intersection {
    cylinder {P1, P2, R1 #if(O1) open #end texture {T} #if(VMD_clip_on[1]) clipped_by {VMD_clip[1]} #end no_shadow}
    VMD_clip[2]
  }
  #else
  cylinder {P1, P2, R1 #if(O1) open #end texture {T} #if(VMD_clip_on[1]) clipped_by {VMD_clip[1]} #end no_shadow}
  #end
#end
#macro VMD_cone (P1, P2, R1, C1)
  #local T = texture { pigment { C1 } }
  #if(VMD_clip_on[2])
  intersection {
    cone {P1, R1, P2, VMD_line_width texture {T} #if(VMD_clip_on[1]) clipped_by {VMD_clip[1]} #end no_shadow}
    VMD_clip[2]
  }
  #else
  cone {P1, R1, P2, VMD_line_width texture {T} #if(VMD_clip_on[1]) clipped_by {VMD_clip[1]} #end no_shadow}
  #end
#end
#macro VMD_triangle (P1, P2, P3, N1, N2, N3, C1)
  #local T = texture { pigment { C1 } }
  smooth_triangle {P1, N1, P2, N2, P3, N3 texture {T} #if(VMD_clip_on[1]) clipped_by {VMD_clip[1]} #end no_shadow}
#end
#macro VMD_tricolor (P1, P2, P3, N1, N2, N3, C1, C2, C3)
  #local NX = P2-P1;
  #local NY = P3-P1;
  #local NZ = vcross(NX, NY);
  #local T = texture { pigment {
    average pigment_map {
      [1 gradient x color_map {[0 rgb 0] [1 C2*3]}]
      [1 gradient y color_map {[0 rgb 0] [1 C3*3]}]
      [1 gradient z color_map {[0 rgb 0] [1 C1*3]}]
    }
    matrix <1.01,0,1,0,1.01,1,0,0,1,-.002,-.002,-1>
    matrix <NX.x,NX.y,NX.z,NY.x,NY.y,NY.z,NZ.x,NZ.y,NZ.z,P1.x,P1.y,P1.z>
  } }
  smooth_triangle {P1, N1, P2, N2, P3, N3 texture {T} #if(VMD_clip_on[1]) clipped_by {VMD_clip[1]} #end no_shadow}
#end
camera {
  orthographic
  location <0.0000, 0.0000, -2.0000>
  look_at <-0.0000, -0.0000, 2.0000>
  up <0.0000, 3.0000, 0.0000>
  right <6.0969, 0.0000, 0.0000>
}
light_source { 
  <-0.1000, 0.1000, -1.0000> 
  color rgb<1.000, 1.000, 1.000> 
  parallel 
  point_at <0.0, 0.0, 0.0> 
}
light_source { 
  <1.0000, 2.0000, -0.5000> 
  color rgb<1.000, 1.000, 1.000> 
  parallel 
  point_at <0.0, 0.0, 0.0> 
}
background {
  color rgb<0.600, 0.600, 0.600>
}
#default { texture {
 finish { ambient 0.000 diffuse 0.650 phong 0.1 phong_size 40.000 specular 0.500 }
} }
#declare VMD_line_width=0.0020;
// MoleculeID: 0 ReprID: 0 Beginning VDW
VMD_sphere(<-2.5073,-0.7283,-0.0000>,0.0990,rgbt<0.000,0.760,1.000,0.000>)
VMD_sphere(<-2.5161,-0.5086,-0.0000>,0.0990,rgbt<0.000,0.760,1.000,0.000>)
VMD_sphere(<-2.5073,-0.2802,-0.0000>,0.0990,rgbt<0.000,0.760,1.000,0.000>)
VMD_sphere(<-2.5073,-0.0518,-0.0000>,0.0990,rgbt<0.000,0.760,1.000,0.000>)
VMD_sphere(<-2.5073,0.1679,-0.0000>,0.0990,rgbt<0.000,0.760,1.000,0.000>)
VMD_sphere(<-2.5073,0.3963,-0.0000>,0.0990,rgbt<0.000,0.760,1.000,0.000>)
VMD_sphere(<-2.5161,0.6248,-0.0000>,0.0990,rgbt<0.000,0.760,1.000,0.000>)
VMD_sphere(<-2.3052,0.5106,-0.0000>,0.0990,rgbt<0.000,0.760,1.000,0.000>)
VMD_sphere(<-2.2262,0.2997,-0.0000>,0.0990,rgbt<0.000,0.760,1.000,0.000>)
VMD_sphere(<-2.1471,0.0888,-0.0000>,0.0990,rgbt<0.000,0.760,1.000,0.000>)
VMD_sphere(<-2.0504,-0.1221,-0.0000>,0.0990,rgbt<0.000,0.760,1.000,0.000>)
VMD_sphere(<-1.9714,-0.3417,-0.0000>,0.0990,rgbt<0.000,0.760,1.000,0.000>)
VMD_sphere(<-1.8747,-0.5526,-0.0000>,0.0990,rgbt<0.000,0.760,1.000,0.000>)
VMD_sphere(<-1.2421,-0.7283,-0.0000>,0.0990,rgbt<0.000,0.760,1.000,0.000>)
VMD_sphere(<-1.2333,-0.5086,-0.0000>,0.0990,rgbt<0.000,0.760,1.000,0.000>)
VMD_sphere(<-1.2421,-0.2802,-0.0000>,0.0990,rgbt<0.000,0.760,1.000,0.000>)
VMD_sphere(<-1.2421,-0.0518,-0.0000>,0.0990,rgbt<0.000,0.760,1.000,0.000>)
VMD_sphere(<-1.2421,0.1679,-0.0000>,0.0990,rgbt<0.000,0.760,1.000,0.000>)
VMD_sphere(<-1.2421,0.3963,-0.0000>,0.0990,rgbt<0.000,0.760,1.000,0.000>)
VMD_sphere(<-1.2333,0.6248,-0.0000>,0.0990,rgbt<0.000,0.760,1.000,0.000>)
VMD_sphere(<-1.4442,0.5106,-0.0000>,0.0990,rgbt<0.000,0.760,1.000,0.000>)
VMD_sphere(<-1.5233,0.2997,-0.0000>,0.0990,rgbt<0.000,0.760,1.000,0.000>)
VMD_sphere(<-1.6023,0.0888,-0.0000>,0.0990,rgbt<0.000,0.760,1.000,0.000>)
VMD_sphere(<-1.6990,-0.1221,-0.0000>,0.0990,rgbt<0.000,0.760,1.000,0.000>)
VMD_sphere(<-1.7781,-0.3417,-0.0000>,0.0990,rgbt<0.000,0.760,1.000,0.000>)
VMD_sphere(<-0.8848,-0.7459,-0.0000>,0.0990,rgbt<0.000,0.760,1.000,0.000>)
VMD_sphere(<-0.8936,-0.5174,-0.0000>,0.0990,rgbt<0.000,0.760,1.000,0.000>)
VMD_sphere(<-0.8936,-0.2890,-0.0000>,0.0990,rgbt<0.000,0.760,1.000,0.000>)
VMD_sphere(<-0.8848,-0.0605,-0.0000>,0.0990,rgbt<0.000,0.760,1.000,0.000>)
VMD_sphere(<-0.8848,0.1679,-0.0000>,0.0990,rgbt<0.000,0.760,1.000,0.000>)
VMD_sphere(<-0.8848,0.3963,-0.0000>,0.0990,rgbt<0.000,0.760,1.000,0.000>)
VMD_sphere(<-0.8848,0.6336,-0.0000>,0.0990,rgbt<0.000,0.760,1.000,0.000>)
VMD_sphere(<-0.6476,0.6248,-0.0000>,0.0990,rgbt<0.000,0.760,1.000,0.000>)
VMD_sphere(<-0.4103,0.6248,-0.0000>,0.0990,rgbt<0.000,0.760,1.000,0.000>)
VMD_sphere(<-0.1907,0.5633,-0.0000>,0.0990,rgbt<0.000,0.760,1.000,0.000>)
VMD_sphere(<-0.0677,0.3612,-0.0000>,0.0990,rgbt<0.000,0.760,1.000,0.000>)
VMD_sphere(<-0.0765,0.1240,-0.0000>,0.0990,rgbt<0.000,0.760,1.000,0.000>)
VMD_sphere(<-0.1995,-0.0781,-0.0000>,0.0990,rgbt<0.000,0.760,1.000,0.000>)
VMD_sphere(<-0.4455,-0.1484,-0.0000>,0.0990,rgbt<0.000,0.760,1.000,0.000>)
VMD_sphere(<-0.6651,-0.1572,-0.0000>,0.0990,rgbt<0.000,0.760,1.000,0.000>)
VMD_sphere(<0.2340,-0.7283,-0.0000>,0.0990,rgbt<0.000,0.760,1.000,0.000>)
VMD_sphere(<0.2252,-0.5086,-0.0000>,0.0990,rgbt<0.000,0.760,1.000,0.000>)
VMD_sphere(<0.2340,-0.2802,-0.0000>,0.0990,rgbt<0.000,0.760,1.000,0.000>)
VMD_sphere(<0.2340,-0.0518,-0.0000>,0.0990,rgbt<0.000,0.760,1.000,0.000>)
VMD_sphere(<0.2340,0.1679,-0.0000>,0.0990,rgbt<0.000,0.760,1.000,0.000>)
VMD_sphere(<0.2340,0.3963,-0.0000>,0.0990,rgbt<0.000,0.760,1.000,0.000>)
VMD_sphere(<0.2252,0.6248,-0.0000>,0.0990,rgbt<0.000,0.760,1.000,0.000>)
VMD_sphere(<0.4361,0.5106,-0.0000>,0.0990,rgbt<0.000,0.760,1.000,0.000>)
VMD_sphere(<0.5152,0.2997,-0.0000>,0.0990,rgbt<0.000,0.760,1.000,0.000>)
VMD_sphere(<0.5942,0.0888,-0.0000>,0.0990,rgbt<0.000,0.760,1.000,0.000>)
VMD_sphere(<0.6909,-0.1221,-0.0000>,0.0990,rgbt<0.000,0.760,1.000,0.000>)
VMD_sphere(<0.7700,-0.3417,-0.0000>,0.0990,rgbt<0.000,0.760,1.000,0.000>)
VMD_sphere(<0.8666,-0.5526,-0.0000>,0.0990,rgbt<0.000,0.760,1.000,0.000>)
VMD_sphere(<1.4992,-0.7283,-0.0000>,0.0990,rgbt<0.000,0.760,1.000,0.000>)
VMD_sphere(<1.5080,-0.5086,-0.0000>,0.0990,rgbt<0.000,0.760,1.000,0.000>)
VMD_sphere(<1.4992,-0.2802,-0.0000>,0.0990,rgbt<0.000,0.760,1.000,0.000>)
VMD_sphere(<1.4992,-0.0518,-0.0000>,0.0990,rgbt<0.000,0.760,1.000,0.000>)
VMD_sphere(<1.4992,0.1679,-0.0000>,0.0990,rgbt<0.000,0.760,1.000,0.000>)
VMD_sphere(<1.4992,0.3963,-0.0000>,0.0990,rgbt<0.000,0.760,1.000,0.000>)
VMD_sphere(<1.5080,0.6248,-0.0000>,0.0990,rgbt<0.000,0.760,1.000,0.000>)
VMD_sphere(<1.2971,0.5106,-0.0000>,0.0990,rgbt<0.000,0.760,1.000,0.000>)
VMD_sphere(<1.2181,0.2997,-0.0000>,0.0990,rgbt<0.000,0.760,1.000,0.000>)
VMD_sphere(<1.1390,0.0888,-0.0000>,0.0990,rgbt<0.000,0.760,1.000,0.000>)
VMD_sphere(<1.0423,-0.1221,-0.0000>,0.0990,rgbt<0.000,0.760,1.000,0.000>)
VMD_sphere(<0.9633,-0.3417,-0.0000>,0.0990,rgbt<0.000,0.760,1.000,0.000>)
VMD_sphere(<2.8464,0.5457,-0.0000>,0.0990,rgbt<0.000,0.760,1.000,0.000>)
VMD_sphere(<2.6567,0.6248,-0.0000>,0.0990,rgbt<0.000,0.760,1.000,0.000>)
VMD_sphere(<2.4511,0.6485,-0.0000>,0.0990,rgbt<0.000,0.760,1.000,0.000>)
VMD_sphere(<2.2376,0.6248,-0.0000>,0.0990,rgbt<0.000,0.760,1.000,0.000>)
VMD_sphere(<2.0557,0.5141,-0.0000>,0.0990,rgbt<0.000,0.760,1.000,0.000>)
VMD_sphere(<1.9292,0.3559,-0.0000>,0.0990,rgbt<0.000,0.760,1.000,0.000>)
VMD_sphere(<1.8738,0.1503,-0.0000>,0.0990,rgbt<0.000,0.760,1.000,0.000>)
VMD_sphere(<1.8580,-0.0553,-0.0000>,0.0990,rgbt<0.000,0.760,1.000,0.000>)
VMD_sphere(<1.8738,-0.2609,-0.0000>,0.0990,rgbt<0.000,0.760,1.000,0.000>)
VMD_sphere(<1.9529,-0.4507,-0.0000>,0.0990,rgbt<0.000,0.760,1.000,0.000>)
VMD_sphere(<2.0952,-0.6009,-0.0000>,0.0990,rgbt<0.000,0.760,1.000,0.000>)
VMD_sphere(<2.2771,-0.7037,-0.0000>,0.0990,rgbt<0.000,0.760,1.000,0.000>)
VMD_sphere(<2.4748,-0.7195,-0.0000>,0.0990,rgbt<0.000,0.760,1.000,0.000>)
VMD_sphere(<2.6804,-0.6958,-0.0000>,0.0990,rgbt<0.000,0.760,1.000,0.000>)
VMD_sphere(<2.8544,-0.5930,-0.0000>,0.0990,rgbt<0.000,0.760,1.000,0.000>)
// End of POV-Ray 3.x generation 
