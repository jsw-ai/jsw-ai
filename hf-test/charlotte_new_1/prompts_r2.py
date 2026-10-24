import json
exec(open('prompts.py').read().split("reqs=[]")[0])
C2=COMMON.replace("visible pores, tiny freckles, uneven skin tone, flyaway hair strands, matte not glossy","smooth youthful healthy skin with tiny freckles across nose and cheeks, matte not glossy").replace("Do NOT copy its big smile: use the expression below.","Faithful recognisable likeness of photo 1: same young face shape, nose, lips, eyes and eyebrows, only the expression changes as described below.")
EX={"c1":"gentle one-sided half-smile, lips slightly parted with a small hint of teeth, one eyebrow slightly raised, looking straight into the camera.",
"c2":"soft amused half-smile, lips slightly parted with a small hint of teeth, chin slightly down, looking straight into the camera.",
"c3":"cheeky half-smile, lips slightly parted with a small hint of teeth, eyebrows slightly raised, looking straight into the camera."}
reqs=[]
for i,(k,(sc,ex)) in enumerate(S.items(),1):
    reqs.append({"index":i,"params":{"model":"seedream_v5_pro","prompt":sc+" "+C2.replace("{EXPR}",EX[k[:2]]),"aspect_ratio":"3:4","count":1,"medias":[{"value":"89826226-7428-42e6-9945-f90d3c090a0a","role":"image"},{"value":"8ed8f1e4-39a1-4488-87e3-82f90f11038c","role":"image"}]}})
json.dump(reqs,open('reqs_r2.json','w'))
print(reqs[0]['params']['prompt'])
