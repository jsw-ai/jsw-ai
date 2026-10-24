# ZenCreator PhotoShoot — live app recon (logged_in = FALSE)

Date: 2026-08-30. URL: https://app.zencreator.pro/tools/photo-shoot
Header shows "Log in" / "Sign up" => NOT authenticated. No credit balance visible anywhere.
Clicking "Select PhotoShoot Category" immediately opens the auth modal
("Create an account to start generating" / Login | Register, HubID, Google, email+password,
18+ / Terms + Content Policy checkbox). So the category/theme grid is gated behind login —
theme names could NOT be enumerated. No generation attempted, no credits spent.

## Right-hand "PhotoShoot Settings" panel (exact copy, visible pre-login)
1. * Face image — "A clear, well-lit face photo used as the source face for generation."
   Dropzone: "Drop your photo here or select a single file / Upload a single file."
   Buttons: [Upload] [Personas v]   (Personas picker only on the FACE slot)
2. * Body image — "A reference photo with the desired pose, clothing, and body composition."
   Dropzone + [Upload]  (no Personas button)
   Both slots carry the rights notice: "You may only upload materials for which you have all
   necessary rights and permissions. Content involving minors or non-consensual content is
   strictly prohibited."
3. PhotoShoot Category — "Set how many images to generate per category. Set to 0 to skip."
   Control: [+ Select PhotoShoot Category]  (badge "New") -> opens picker (login-gated).
   => image count is set PER CATEGORY inside that picker; 0 = skip.
4. Aspect Ratio — "Select the width-to-height ratio for the output images." Default 3:4 (dropdown).
   (No separate "resize" control visible pre-login.)
5. [Generate PhotoShoot (0 images)]  hotkey Ctrl+Enter ; caption under button: "3 credits per image".
   Counter in the button = total images summed across categories.
6. Trash icon top-right of panel = reset settings.

## Reference-slot mapping (per Sam's rule)
- PhotoShoot: TWO slots -> use BOTH: face shot in "Face image", front-facing FULL BODY in "Body image".
  Body image also drives pose/clothing/body composition, so choose the body ref for the look you want.
- Marketing "How It Works" on the same page: "Step 1: Upload Your Selfie and Full-Body Pictures"
  -> confirms face + full-body pairing. Step 2: Choose Your Style. Step 3: Get Your Headshots.
- Other tools' slot counts not verified (login-gated); assume single-ref tools (Reference-To-Image,
  Image Editor, Variations, Face Generator) need a front-facing FULL BODY ref.

## Templates library (left/main area, tab: Tasks | Gallery | Library, searchable)
Tag chips available: photoshoot, girl, man, Portrait, professional, style, winter, travel, car,
outdoor, anime, blondy, casual, cinematic, retro, selfie, superhero, carnival, classic, home, office,
snow, suit, art, cosplay, elegance, fashion, leather, sport, street, street style, underwear, urban,
vibes, angel, auto, biker, boss, cabin, cinema, circus, city, clasic, club, coffee, comfort,
confidence, costume, cozy, cozy home, cyberpunk, Dance, deadpool, dentist, evening, gallery,
gladiator, grocery, indoor, jeans, magic, medic, modern, morning, mountain, neon, night, park, pink,
profile, profile photos, racer, rome, rooftop, run, seaside, show, siteview, sporty, standing,
street-food, studio, suits, summer, sunset, train, twilight, vibe, view, walk, work (+ Expand filters).
Visible template cards: Winter; Elegance among sculptures; Underwear photo shoot; Portrait;
Professional; Day in the office; Night out; Man at home; Elegance in the city; Cinematic;
Profile photos; Velvet lounge relaxation; Dentist girl; Winter cabin portrait; Morning coffee dose;
Template; Elegance at twilight pavilion; Anime; She's a doctor; Classic style professional;
Color pop-street energy; Cozy home; Out of office; Seaside selfie.
Each card: [Try Template] [copy prompt] [like]. No Female/Male split and no 18+/NSFW/Lingerie/
Bikini/Glamour/Nude grouping is exposed pre-login; closest spicy items = "underwear" tag +
"Underwear photo shoot" template.

## Tools list (sidebar + /tools cards)
Video: Image-To-Video, Video-To-Video, Video Upscaler, Lipsync, AI Video Merger.
Image: Text-To-Image, Image Editor, Image Upscaler, Reference-To-Image, PhotoShoot, Face Generator,
Variations, Collabs. Plus: Explore, My Generations, Companion, Guides, AI University, Personas,
Posts, MCP Server (BETA, mcp.zencreator.pro).
