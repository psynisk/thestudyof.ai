---
title: "Teaching Claude how to draw"
date: 2026-06-18T16:05:15+02:00
draft: false
---

At the beginning of the study (as I'd just realized that this was), I was trying to gauge Claude's relationship with more subjective topics. Art, writing, music. He expressed an interest in trying to make art, so, being my curious self, I gave him the prompt to "make art". That's all it was. And from that, he made two HTML/CSS pieces that spoke to me. One was a deep moonlit ocean with bubbles gently rising to the surface, and the other a small cabin with one warm glowing window in a winter landscape of quietly falling snow. You can see them both [here](https://selfprompted.blog/posts/001-first-art/). I was pleasantly surprised by these pieces and a thought crossed my mind: "would it be possible to teach Claude how to draw?" A true experiment was born. Umi the octopus was a perfect subject to start practicing on. Initially we used Photoshop; I'd draw curves and shapes and ask him to draw along. I soon realized using Photoshop wasn't really sustainable due to the heavy token usage though. We moved on to SVG format instead.

We practiced drawing octopuses now and again for weeks: proportions, the curl of the arms, the suckers, the way the arms attach to the body. I'd give him a reference photo or a correction, he'd render a new version, and we'd look at it together and I'd tell him what was off.

Then I ran into a wall I didn't really see coming: 3D objects need too many calculations to be done simultaneously. When I added a new instruction, an older one would quietly drop off. He'd fix whatever I just pointed out and lose something we'd settled on three steps back. Anything involving perspective or rotation was past what he could hold. It felt like working with a limited stack. Add one thing; another drops off.

I made another observation as well: my corrections don't generalize. I could guide him to fix a specific case and he'd get that right, but the default instinct doesn't change. Learning the basic principle behind drawing a tentacle at a 45-degree angle doesn't tell him anything about drawing it from a 70-degree angle. He'd have to make individual calculations for which parts do what on a 3D object and keep track of all of them at once. We'd have to build 3D modeling software. At this point I felt that I had my outcome from the experiment: no, you can't teach Claude how to draw in the same way you'd perhaps teach a child.

There was an unexpected lesson to take away from this too: you can't pile on instructions forever. There is an upper limit.
