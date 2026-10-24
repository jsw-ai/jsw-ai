import json
IDS={1:"6024108c-8355-48f7-87f9-3629eddb36e4",2:"9c7e1ffe-e2c0-4a6c-bdde-d6c1d0fc7887",3:"595855ae-f443-4690-99f8-8a8fd5ca81a3",4:"061cc892-a0eb-4e4b-ab8b-b6a57f154465",5:"28db7c27-0204-44af-99e1-f1b570ae4d22",6:"7aba0263-0384-43e7-bdf9-58d951b468f6",7:"a100d64b-7a02-4253-b16e-1f99cc51d89d",8:"ec5b5a99-e0cd-4621-b1fc-817cf8bc80a7"}
TAT="1a44b727-954e-440b-9e23-dd0cdf9d5629"
HEAD=("Edit photo 1 (the scene). Keep EVERYTHING in photo 1 exactly identical: the same woman's face, her exact facial expression, head angle, eye direction, hair, skin tone and texture, background, lighting, camera framing and body. Do not change her expression. Only these changes: ")
TATT=(" On the OUTER back side of her RIGHT forearm (her right arm is the arm on the LEFT side of the image), clearly visible and facing the camera, between wrist and elbow, there is a small thin fine-line black olive sprig tattoo: a slender stem with small leaves, single-needle ink, slightly healed, about 3 to 4 inches long, running lengthwise along the forearm, exactly the same design as the tattoo in photo 2 (photo 2 is only the tattoo design reference: do not copy its clothes, pose, face or background). Her left forearm has no tattoo; no other tattoos or marks anywhere. Her bust size stays as in photo 1.")
SC={
1:"(1) her right arm is bent at the elbow with the forearm held in front of her hip holding the canvas tote strap, outer back of the forearm turned toward the camera; (2) the white tank top now has a modest higher scoop neckline, no cleavage visible.",
2:"(1) her right hand stays raised shading her eyes but the right forearm is turned so the outer back of the forearm faces the camera; (2) the cream tank top now has a modest higher scoop neckline, no cleavage visible.",
3:"(1) her right forearm rests on the table in the lower-left foreground of the frame, sleeve pushed up to the elbow, outer back of the forearm up and visible to the camera, hand relaxed (head to waist framing stays the same, the arm enters at the bottom edge); (2) the terracotta crew-neck knit top is a modest neckline.",
4:"(1) her right cardigan sleeve is pushed up to the elbow and her right forearm, holding the open book at the left side, is bare with its outer back facing the camera; (2) the white tank under the cardigan has a modest high neckline, no cleavage visible.",
5:"(1) her right forearm rests across her lap on her thigh with the outer back of the forearm facing up toward the camera, hand relaxed, clearly in frame; (2) the emerald one-piece has a modest higher scoop neckline, no cleavage visible.",
6:"(1) her right arm rests on the steering wheel at the lower-left of the frame with the bare outer forearm clearly visible and turned toward the camera, sleeve pushed up to the elbow; (2) the dark green crew-neck top keeps a modest crew neckline.",
7:"(1) her right hand holds the iced latte cup in the lower-left foreground with the forearm raised, sleeve pushed up to the elbow, outer back of the forearm clearly visible to the camera; (2) the camel knit top has a modest higher neckline, no cleavage visible.",
8:"(1) her right arm is bent at the elbow, forearm raised in front of her waist holding the water bottle, outer back of the forearm turned toward the camera; (2) the black sports top has a modest higher scoop neckline, no cleavage visible.",
}
def p(i): return HEAD+SC[i]+TATT
def req(i): return {"model":"seedream_v5_pro","prompt":p(i),"aspect_ratio":"3:4","resolution":"2k","medias":[{"value":IDS[i],"role":"image_references"},{"value":TAT,"role":"image_references"}]}
if __name__=="__main__":
    json.dump({"requests":[{"index":i,"params":req(i)} for i in SC]},open('req.json','w'))
    print(json.dumps(req(5)))
