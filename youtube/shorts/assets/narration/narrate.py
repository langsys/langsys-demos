"""
Front every web demo with the intro and narrate it.

For each demo: generate the narration with the Emma neural voice, place each
line on that demo's own scene boundary shifted by the intro's length, mix it
under the intro sting, concatenate intro + demo video, and mux.

Scene boundaries are copied from each master's SCENES table. They are the
contract — a line that runs past its scene is narrating the wrong picture, so
every line is measured against its window and flagged before anything encodes.

Voice is per demo, and every demo now uses the same one: Andrew, the voice
the explainer was cut with. The feature cuts used to carry Emma, which made
the library sound like two products the moment a viewer went from the
explainer to any other cut. Set `voice=` on a demo to override.

`groups=` is what makes a read sound like an explanation instead of a list.
Synthesized a line at a time, every line gets a fresh start, a full
sentence-final fall, and then dead air until the next beat — the result is
someone reading captions aloud. Grouped, each run of lines is sent to the
service as one utterance, so intonation carries across it and the pauses are
the voice's own. `groups=[2, 2, 4, 4, 4]` reads sixteen lines as five breaths,
one per act, and each group re-anchors on its first beat so timing drift cannot
accumulate past the end of an act.

The catch is that a continuous read has no long pause to absorb a mistimed
line. **Write each line to last as long as its beat, not merely to fit inside
it** — a short line pulls everything after it early, onto the picture before its
own. The report prints a fill percentage for exactly this; aim for 90–100%, and
treat STARTS EARLY as seriously as OVERRUNS.

Which leads to the rule that matters most on the short cuts: **`starts` are
narration windows, not scene boundaries, and one line per beat is not the
goal.** Under about 3 seconds a window only holds ~8 words, and the only way to
fit is to drop the verb — which is how you get "No gender data, the neutral
branch." Fragments like that are what a viewer hears as a robot reading
captions, and no amount of timing work fixes them. When the picture cuts faster
than a sentence can be spoken, give one sentence several beats and let the
narration flow across the cuts. Some beats then go unnarrated; that is correct,
because the picture and its caption are already saying it.

Run with no argument to build every demo, or `python narrate.py explainer` for
one. A demo can only be built if its silent body is already encoded to
BASE\body-<name>.mp4 — the frames are git-ignored, so that step comes first:

    ffmpeg -y -framerate <FPS> -i frames-<name>/%03d.png \
           -c:v libx264 -preset slow -crf 18 -pix_fmt yuv420p \
           -r 30 -movflags +faststart <BASE>/body-<name>.mp4
"""

import asyncio
import math
import os
import re
import subprocess
import wave

import numpy as np
from scipy import signal
import edge_tts

SR = 48000
# One narrator for the whole library. A Multilingual voice, which is what
# keeps 'Inicio', 'Hogar' and 'Bienvenido' from being read with an English
# mouth. Andrew reads a touch slower than Emma did, so lines tuned for her
# tend to fill their beats more fully — check the report after any change.
VOICE = "en-US-AndrewMultilingualNeural"
VOICE_M = VOICE
# Two rates, one voice. The feature cuts were timed against Emma at +8%, and
# Andrew at the same setting reads about a tenth slower — 65 lines ran past
# their beats on the first library-wide pass. +15% brings him back to the
# pace those beats were written for. The explainer keeps +8%, which is the
# read everyone liked; set `rate=` on a demo to override.
RATE = "+15%"
RATE_EXPLAINER = "+8%"

# How the product name is said. The scripts keep the written name and the
# voice is handed a respelling: Andrew reads "Langsys" as "Lang-sees", and the
# name is "Lang-sis". edge-tts takes no phoneme markup, so a spelling is the
# only lever. Of six respellings rendered with this voice, the team picked
# "Langsis" (2026-09-14). assets/tour/narrate_tour.py carries the same table;
# keep the two in step.
SAY_AS = [(re.compile("langsys", re.I), "Langsis")]


def spoken(text):
    """The text as the voice should read it, with every SAY_AS respelling
    applied. Stops the build if the written name would still reach the voice."""
    for pattern, say in SAY_AS:
        text = pattern.sub(say, text)
    assert "langsys" not in text.lower(), f"the written name would be spoken: {text!r}"
    return text

REPO = r"C:\laragon\www\langsys-demo-videos"
BASE = r"C:\Users\gianc\AppData\Local\Temp\claude\C--laragon-www-langsys-demo-videos\87515e3b-fede-40e5-b744-7d2910bf36b0\scratchpad"
FF = os.path.expandvars(
    r"%USERPROFILE%\AppData\Roaming\Python\Python311\site-packages"
    r"\imageio_ffmpeg\binaries\ffmpeg-win64-v4.2.2.exe")

INTRO_MP4 = os.path.join(REPO, "assets", "intro", "intro-16x9.mp4")
INTRO_WAV = os.path.join(REPO, "assets", "intro", "intro-sting.wav")
INTRO_LEN = 3.60

# name, dir, total seconds, scene start times, narration lines.
# starts[i] is when line i's scene begins; the window ends at starts[i+1]
# (or the demo's end for the last one).
DEMOS = [
    # Twelve beats. The cut opened after the damage was already done — on
    # another library's call, with the sentence already gone — so it never
    # showed the thing it spends the rest of its length getting back. It now
    # starts on the plain sentence. Category and plurals also get shown rather
    # than described: the Inicio/Hogar pair and the Russian ladder were both
    # facts stated in a note while the panel rendered something else.
    dict(name="t-string", dir=r"svelte\web\t-string", secs=65.75,
         groups=[4, 4, 2, 2],
         starts=[2, 7, 11.5, 16.75, 22.25, 27.25, 32.5, 37.75, 43, 47.25, 52.25, 57.25],
         lines=[
             "You start with just one plain sentence, written in whatever language your app already uses today.",
             "Every other library asks you to invent a name for it before it will translate anything.",
             "That sentence then moves away into a separate file, and the name left in your code points across at it.",
             "Rename one and forget the other, and nothing breaks, the user just reads your variable name.",

             "Langsys deletes that invented name, because you hand it the sentence you already wrote.",
             "The first argument is the sentence itself, and that very same sentence is also the key.",
             "The second is a category, because Home in a menu and Home the house are two different words in Spanish.",
             "And the third is your values, where the curly braces in the sentence are the slots they fill.",

             "Switch the locale, and that very same call comes back to you in Spanish.",
             "Every language you turn on comes out of the one line, with nothing new to wire up.",

             "Some languages, though, need more wordings, and Russian needs four altogether.",
             "So you write the sentence flat, with just the count in it, and Langsys builds the forms each locale needs.",
         ]),
    # 36s rewrite. The old cut assumed a viewer who had already watched
    # `t-string`: it left `category` on screen unexplained, and it dropped the
    # inline <b> the moment <Phrase> appeared, so the tag never solved the
    # problem the tag exists for. Three windows are new — the reorder proof,
    # the category, and where the Spanish came from — which is why it runs
    # nine seconds longer than the version it replaces.
    # Three problem beats instead of one, and the marker mechanism said out
    # loud. The cut used to carry the cut-at-the-tag argument, the fragments
    # and the word-order consequence inside a single note, then jump to the
    # answer — so the payoff landed before the problem had been felt.
    dict(name="phrase-tag", dir=r"svelte\web\phrase-tag", secs=62.75,
         groups=[3, 3, 2, 1, 2],
         starts=[2, 7.75, 12.5, 18.25, 23.5, 28.75, 33.5, 38.5, 43.75, 49.75, 54.25],
         lines=[
             "A sentence with a bold word in it is still one sentence, but other libraries cannot keep it that way.",
             "They cut it at the tag, so your translator gets three fragments and never reads the sentence.",
             "And word order moves between languages, so gluing those back in English order is already wrong.",

             "Now with Langsys, you wrap the whole run instead, markup and all, in one single tag.",
             "Your bold never reaches the translator, because Langsys swaps it for a neutral marker first.",
             "So it can move that marker, and in Spanish your bold lands after the noun instead of before it.",

             "Alongside it, the category goes over, so a translator knows which sense you meant.",
             "And your runtime values come in through params, a plain object beside the sentence.",

             "One catch in markup, though, the placeholders are percent name, because braces belong to Svelte itself.",

             "Switch the locale, and your tags and your classes stay exactly where you put them.",
             "And you never wrote that Spanish, the phrase registered itself the first time this component ran.",
         ]),
    # From-scratch version. Two beats now establish what is even being looked
    # at before any library appears: the section as a reader sees it, then the
    # same thing as two runs of text with the runs lit. `run of text` and
    # `content block` are the two terms the whole cut rests on and neither was
    # ever defined; `category` appeared in the code and was never mentioned.
    dict(name="translate-tag", dir=r"svelte\web\translate-tag", secs=60,
         groups=[2, 3, 4, 2],
         starts=[2, 6.75, 11.75, 16.5, 21.25, 26.25, 31.5, 36.75, 42.25, 46.75, 51.25],
         lines=[
             "Here is a section of one of your pages, a heading with a short paragraph sitting underneath it.",
             "In your markup that is two separate runs of text, with tags holding them apart.",

             "Other libraries make you invent a name for each of those runs, and call them up one at a time.",
             "So your translator receives them as two separate little jobs, in no particular order.",
             "So the word shipping comes back as two different Spanish words, one in each of them.",

             "Now with Langsys, you put one single tag around the whole region, and you change nothing inside it.",
             "And the category travels along as context, telling the translator what this part of the app is.",
             "Langsys then sends the sentences over on their own, and keeps your tags here as numbered positions.",
             "So the whole section arrives as one job, laid out the way a reader meets it.",

             "Switch the locale, and both of them follow, with your tags dropped back around them.",
             "And because both sentences went over together, shipping is the same word in both.",
         ]),
    # 28s rewrite. The 17s read was six clipped declaratives over six sub-3s
    # beats -- "So you wrap it once, and only once." / "The sentence around it
    # still moves." -- which is the exact failure this file's docstring warns
    # about: no connective tissue, so it lands as a robot reading the captions.
    # Wider windows, sentences that carry into each other, and a middle act that
    # takes the competition's best answer seriously before beating it.
    dict(name="donttranslate", dir=r"svelte\web\donttranslate", secs=30,
         groups=[2, 2, 3],
         starts=[2, 6.5, 11, 15.5, 20, 24.5, 28],
         lines=[
             "A translator has no way of knowing that Bright Ledger is a product, not a phrase.",
             "So it gets translated, and your brand quietly changes in every market.",

             "Other libraries ship it just like that, and the only way out is lifting the name out.",
             "Now with Langsys, you simply mark the part that must not move.",

             "That whole subtree then comes back exactly as written, in every locale.",
             "And the sentence around it still translates and reorders.",
             "Your brand, left alone.",
         ]),
    # ICU plurals. The eight beats run 1.75-2.75s each, far too short to hold
    # a sentence apiece, so the narration uses four wider windows and lets one
    # sentence run across the three Russian number changes.
    # Gender agreement. Six beats of 2.5-3.5s, so four narration windows: the
    # three user swaps read as one sentence rather than three fragments.
    # 33.5s rewrite. The old read was five lines, two of them starting "So",
    # over beats as short as 2.5s -- and it opened on the capability, so the
    # branches Langsys generates had nothing to be better than. It now opens on
    # the conditional another library leaves in your component, and the payoff
    # beat has room to say who wrote the Spanish.
    dict(name="icu-gender", dir=r"svelte\web\icu-gender", secs=35.5,
         groups=[2, 2, 2, 2],
         starts=[2, 6.5, 11, 15, 19, 26, 29.5, 33.5],
         lines=[
             "Spanish adjectives have to agree with the gender of the person you are addressing.",
             "So other i18n leaves you writing that grammar as a conditional in your component.",

             "Now with Langsys, you write one English sentence with no branches in it.",
             "And then you pass in the gender you already hold on the user record.",

             "So Diego gets Bienvenido, Laura gets Bienvenida, and the difference between them is a single value you passed in.",
             "When the record does not say, a neutral welcome answers instead.",

             "And not a single one of those three Spanish branches was ever written by you at all.",
             "Langsys generated all of them.",
         ]),
    # Why categories exist. The argument the library was missing: the invented
    # key in traditional i18n was only ever disambiguating two identical
    # sentences, and the category takes that job over.
    # <Translate> over a whole component. Six 3s beats, so three wide narration
    # windows rather than one line per cut.
    # Every line used to be the same shape: declarative, comma, declarative,
    # three of them opening "So ... instead". Six of those in a row is what
    # reads as a robot -- the sentences are fine one at a time and monotonous
    # end to end. Rewritten for varied rhythm, and beat 1 now names whose
    # problem it is rather than leaving "by hand" to carry it.
    # 36s rewrite. The cut is named after a term it never defined — someone
    # meeting "content block" here had no way to find out what one is, so the
    # beats landed as a list of behaviours rather than a reason to want them.
    # Two new windows carry the definition: what the other approach hands a
    # translator, and what a block actually is (one unit to work on, still made
    # of individually reusable phrases).
    dict(name="content-blocks", dir=r"svelte\web\content-blocks", secs=38,
         groups=[2, 2, 2, 3],
         starts=[2, 6.5, 11, 15.5, 20, 24.5, 29, 33, 36],
         lines=[
             "A component is never one string, it is several, scattered through your markup.",
             "And other i18n hands your translator those pieces as a flat list.",

             "Now with Langsys, you wrap the whole region once and touch nothing inside it.",
             "That region becomes a content block, the whole section registered as one unit.",

             "Inside it, every single run of text is still its own reusable phrase.",
             "Switch the locale, and all of your markup comes back completely intact.",

             "And your brand stays verbatim, because that subtree never leaves.",
             "One tag, a whole region, in every locale.",
             "Nothing inside it was edited.",
         ]),
    # Adding a target locale. The beat that keeps this honest is the last one:
    # adding a locale does not backfill. New phrases are translated on arrival
    # when machine_translate_new_phrases is on; everything already in the
    # project is filled by a separate translate-untranslated run.
    dict(name="adding-a-locale", dir=r"shared\tutorial\adding-a-locale", secs=26,
         groups=[3, 3],
         starts=[2, 6, 10, 14, 18, 22],
         lines=[
             "Which locales you translate into is a setting on the project itself.",
             "So adding Portuguese is one entry, and the column appears empty.",
             "Your app did not change, because nothing was ever bundled into it.",

             "From then on, new phrases are machine translated on arrival.",
             "And one untranslated run fills in everything already there.",

             "So a new language is a settings change, not a build or a deploy.",
         ]),
    # Rebuilt as a from-scratch explanation. The cut assumed the viewer knew
    # what an HTML attribute is — the one thing it cannot assume, since every
    # later beat rests on it. Three beats now define the two kinds of text,
    # and a half-translated Spanish page shows the failure the cut used to
    # only assert.
    dict(name="attributes", dir=r"svelte\web\attributes", secs=63.25,
         groups=[3, 2, 1, 2, 3, 1],
         starts=[2, 6.5, 11, 16, 21, 26.25, 31.75, 37.5, 43, 47, 51.5, 56.25],
         lines=[
             "Look at any form on your site, and you will find its text comes in two different kinds.",
             "There is the text sitting between the tags, which is the part you can actually see there on the page.",
             "And there is text tucked inside a tag itself, and that is what an attribute is.",

             "Translate only the first kind of text, and this is what a Spanish customer really gets from you.",
             "The hint inside the box is still English, and so is everything a screen reader reads out.",

             "Other libraries want a separate call on each attribute, and the one you forget fails quietly.",

             "With Langsys you wrap the whole region once, using the same translate tag as everywhere else.",
             "It then walks everything inside, the visible words and the attributes, in a single pass.",

             "Switch to Spanish, and the hint inside the box comes across with it.",
             "So does the image description, the words read out when the picture cannot be seen.",
             "And so does the label on the button, which is the name a screen reader announces.",

             "And you annotated nothing anywhere to make any of that happen.",
         ]),
    # Numbers and dates. The opt-out is the beat worth having: an order number
    # passed as a Number comes back grouped, and that is a bug someone ships.
    # Same rewrite as content-blocks: the old read was six identical shapes,
    # two of them "So pass ... instead". Beat 1 names the alternative rather
    # than describing the bug in the abstract.
    # Opens on Langsys now -- the hand-rolled problem beat was cut, so the
    # before/after lives in the order-number pair at the end instead. Beats 2
    # and 3 are one breath because they are one point: both separators and
    # dates come out of CLDR, and neither is anything you configure.
    # Rewritten. The cut used to open on "With Langsys" and carry that same
    # chyron on all five beats — no turn, no stakes, just five facts read in a
    # row, which is what made it sound like a list. It now opens on the raw
    # number being wrong, spends a beat on the branch you write by hand, and
    # adds a beat showing CLDR is a set of shapes, not a punctuation swap.
    dict(name="formatting", dir=r"svelte\web\formatting", secs=42.75,
         groups=[2, 3, 1, 2, 1],
         # +2.0 across the board: the title card holds the head of the
         # timeline and no line is spoken over it.
         starts=[2, 6.75, 11.75, 15.75, 20, 24.5, 29.5, 34.5, 38.5],
         lines=[
             "A number printed straight into your interface is already wrong in somebody's locale.",
             "So you branch on the locale by hand, and then you do the same again for every date.",

             "With Langsys you hand over the number itself, and the date as a date.",
             "German, for example, trades the comma for the point, per CLDR.",
             "The date is CLDR as well, month name and punctuation included.",

             "And it goes further than punctuation, because Hindi does not group its digits in threes.",

             "Which is exactly the wrong answer when those digits happen to be an order number, and not a quantity at all.",
             "Pass an id as a string, and it survives untouched.",

             "Pass the real type, and every locale formats it its own way.",
         ]),
    dict(name="categories", dir=r"svelte\web\categories", secs=30.5,
         groups=[2, 2, 2, 1],
         starts=[2, 6, 10, 14, 18, 22.5, 27.5],
         lines=[
             "The very same English word can end up meaning two completely different things.",
             "And this is why i18n invented keys in the first place.",

             "Langsys keeps your sentence and files it under a category instead.",
             "Two categories give you two translations, from the very same phrase.",

             "Free, say, is a price over here, and an evening with nothing booked there.",
             "And an order is a purchase, or the sequence you sorted the table by.",

             "So the key only ever told two sentences apart.",
         ]),
    # 45s rewrite. The 17s cut ran four lines over eight beats, three of them
    # under two seconds — the Russian act changed the number, the noun form and
    # the CLDR category every 1.75s while the narration was still finishing the
    # previous sentence. The picture now holds still long enough for a viewer
    # who has never seen a plural category to be told what one is, and the read
    # is one line per beat rather than one line per three.
    # 70s rewrite. The cut taught you to write ICU branches yourself and then
    # claimed "you wrote two, Langsys wrote the rest" -- which misdescribes the
    # pipeline. OpenRouterTranslationEngine translates FLAT (the translator
    # prompt forbids restructuring), then a second pass rebuilds the target
    # string in the target locale's own categories; when source == target that
    # promotion runs on your own English too. So the honest story is that you
    # write no branches at all, in any language, and the middle act now shows
    # both stages on Russian -- flat first (wrong at one message), then rebuilt.
    dict(name="pluralization", dir=r"shared\web\pluralization", secs=70,
         groups=[3, 2, 1, 1, 2, 3, 1, 2],
         starts=[2, 7, 12, 17, 22, 26.5, 32, 36, 40.5, 44.5, 48, 51.5, 55.5, 60, 65],
         lines=[
             "In English the sentence itself changes with the number, one message but three messages.",
             "So other i18n libraries make you pick between those two, with an if in your code.",
             "And that holds up in English, right up until the sentence leaves English.",

             "Now with Langsys, you write the sentence flat, with no plural branches anywhere in it at all.",
             "And Langsys rebuilds it, starting with your own English.",

             "Because how many forms a language actually has is not something your own code could ever guess.",

             "Spanish, for one, gets two, because Spanish has two.",

             "Russian, though, is translated flat first, wrong at one message.",
             "A second pass then rebuilds it in the four forms Russian has.",

             "Two, three and four take a form that English lacks.",
             "Five right through twenty take a third one, off the same line.",
             "And twenty-one goes back to the singular, because it ends in a one.",

             "The number itself is local too, grouped with spaces here rather than commas.",

             "And the number of plural branches you wrote yourself, in any language at all, is none.",
             "So you could turn on Arabic tomorrow, and this line would not change.",
         ]),
    # 36s rewrite. The 22s cut opened on "every locale gets its own file",
    # which assumes the viewer already accepts that locale files are how i18n
    # works — the premise this module exists to argue against. Two beats now run
    # in front of it: where a project actually starts, and the step other i18n
    # libraries make you take first (inventing a key). The turn names Langsys
    # out loud rather than saying "so delete it".
    dict(name="key-files", dir=r"shared\tutorial\key-files", secs=38,
         # "Now, with Langsys" and "You write the sentence" are read apart: as
         # one breath, the short first line pulled the second onto the
         # bookkeeping picture once the voice's timing moved (2026-10-13).
         groups=[2, 1, 3, 1, 1, 2],
         starts=[2, 6.5, 11, 15, 18.5, 22.5, 25.5, 28.5, 32.5, 36],
         lines=[
             # "a name for it" had no antecedent anyone could hear. The thing
             # being named is the sentence in the h1, which the picture shows
             # from the first frame but the read never mentioned — so the
             # nearest spoken nouns were "app" and "language", and neither is
             # what you invent a name for. Line 1 now plants the sentence and
             # line 2 points back at it. Both are in group 0, one breath.
             "Every project starts here, with one app, one language, one sentence.",
             "Other i18n libraries make you invent a name for that sentence first.",
             "And then every single language you add gets a file of its own.",

             "And there in your code, the sentence itself has simply vanished.",
             "Miss a single key in one file, and this is what your user sees.",
             "None of that is translation, it is bookkeeping.",

             "Now, with Langsys, you get to delete all of it.",
             "You write the sentence, because with Langsys the phrase itself is the key.",

             "Every locale runs off that same line, with nothing to sync.",
             "No keys, and no files.",
         ]),
    dict(name="workflow", dir=r"shared\tutorial\workflow", secs=26,
         groups=[4, 4],
         starts=[2, 5.5, 9, 12, 15.5, 18, 21.5, 24],
         lines=[
             "One language is a feature, but nine is a supply chain.",
             "Every string leaves your codebase, and comes back weeks later.",
             "Now go and change just a single word in that English copy.",
             "And then that entire pipeline has to run all over again.",

             "So Langsys simply deletes that pipeline.",
             "The phrase is the key, translation resolves at runtime.",
             "Change the copy, and it is already showing.",
             "No handoff, and no waiting.",
         ]),
    # The flagship overview — the only cut that explains what Langsys is rather
    # than what one API does, and the only one with its own narrator.
    # Grouped by act, so each act is read as one continuous breath. Lines are
    # written to fill roughly 90% of their beat: the first pass used terse
    # one-clause lines and left ~24s of the 72 in silence, which is what made a
    # good read sound like a list. Each line is one sentence — see synth_group.
    # Beat lengths are deliberately uneven now — 4.0 to 5.5. Every beat used to
    # be 4.5s or 5.0s with one sentence read at ~95% fill, so the picture
    # changed on a metronome and the cut read as a list no matter how the lines
    # were written. The turn ("two pieces") is the short one.
    # Act 3 gained a beat for auto-discovery, which is the one thing in the
    # product that anonymous traffic drives. It costs 5.5s on a cut that was
    # deliberately trimmed twice — worth it, because "your visitors register
    # your content" is the strongest claim Langsys can make and the old copy
    # said the opposite ("a read-only key does not discover").
    # Act 3 is now told as one story — publish a page, a visitor opens it,
    # Langsys comes and reads it — instead of two beats about key types. The
    # key types, the two server answers and the request itself moved down to
    # keys-and-environments; this cut says "cannot write from here" and no more.
    dict(name="explainer", dir=r"shared\web\explainer", secs=73.75, voice=VOICE_M, rate=RATE_EXPLAINER,
         # Act 3 is three breaths: how a phrase registers and the page going
         # up; the visitor and Langsys's visit; then what happens to what
         # arrived. Pairs, because a run of five let each line's shortfall
         # accumulate until the read was 1.3s ahead of its picture.
         groups=[2, 3, 2, 2, 1, 1, 3],
         starts=[2, 6.75, 12.75, 18, 23.5, 28.25, 32.75, 38.25, 43.5, 50.25, 54.75, 59.25, 64.75, 69.25],
         lines=[
             # Present tense, and the cost said out loud. "Used to mean" conceded
             # the turn before the problem had landed, and the two details that
             # actually hurt — weeks, and files that rot silently — were sitting
             # in 15px grey notes that nobody reads at five seconds a beat.
             "Adding a second language to your app means adding a pipeline, measured in weeks.",
             "And a copy of every sentence in every locale file, which quietly drift apart.",

             "Langsys replaces all of that with two pieces, first an SDK inside your app.",
             "And second, a hosted Translation Manager, holding every phrase your app ever ran.",
             "One call answers in every locale, and the phrase itself is the key.",

             "You never register a phrase, a developer running the code with a write key does it.",
             "But what about content no developer runs, say a blog post, published at nine with no build?",

             "A minute later its first reader opens it, and the app sends Langsys only the address.",
             "Langsys then reads the page itself, and minutes later a reader in Madrid gets it in Spanish, with no deploy.",

             "And where the wording matters, a translator can sharpen it in place.",

             "One more thing, the category tells a translator which sense you meant.",

             "Day one is really just three steps, install it, initialize it, and wrap your strings.",
             "And it is the same idea in every SDK, six of them, front and back.",
             "You write English, and your users read their own language.",
         ]),

    # The explainer in Spanish — the pilot for dubbing the library. Same
    # picture (captured with `capture.py explainer --lang=es`, which renders the
    # master's Spanish text), same beats, same voice: Andrew is a Multilingual
    # voice, so the library keeps one narrator across languages. Latin-American
    # neutral, tú, because the Learning Center serves Spanish as es-419.
    # Spanish runs longer than English, so these are written to the English
    # line's length, not translated word for word — the report's fill
    # percentage is what says whether they fit.
    dict(name="explainer-es", dir=r"shared\web\explainer", secs=73.75, voice=VOICE_M, rate=RATE_EXPLAINER,
         groups=[2, 3, 2, 2, 1, 1, 3],
         starts=[2, 6.75, 12.75, 18, 23.5, 28.25, 32.75, 38.25, 43.5, 50.25, 54.75, 59.25, 64.75, 69.25],
         lines=[
             "Agregar un segundo idioma a tu app significa montar todo un proceso que toma semanas.",
             "Y una copia de cada frase en cada archivo de idioma, que poco a poco se desincronizan.",

             "Langsys reemplaza todo eso con dos piezas: primero, un SDK dentro de tu app.",
             "Y segundo, un Translation Manager en la nube, con cada frase que tu app ha usado.",
             "Una sola llamada responde en todos los idiomas, y la frase misma es la clave.",

             "No registras frases: lo hace quien ejecuta el código con una clave de escritura.",
             "¿Y el contenido que nadie ejecuta, como un artículo publicado a las nueve sin compilar nada?",

             "Un minuto después llega su primer lector, y la app solo le envía a Langsys la dirección.",
             "Langsys lee la página por su cuenta, y minutos después alguien en Madrid la lee en español, sin desplegar nada.",

             "Y donde el texto importa, un traductor puede pulirlo ahí mismo.",

             "Algo más: la categoría le dice al traductor qué sentido quisiste dar.",

             "El primer día son tres pasos: instálalo, inicialízalo y envuelve tus textos.",
             "Y es la misma idea en los seis SDKs, de frontend y backend.",
             "Tú escribes en inglés, y tus usuarios leen en su propio idioma.",
         ]),

    # ── The concepts course ────────────────────────────────────────────────
    # docs.langsys.dev/learn/concepts is the one part of the learning centre
    # that runs in a fixed order — each page carries a real Next: button:
    #
    #   how-it-works -> token-discovery -> locale-store -> keys-and-environments
    #
    # Modules 1 and 2 are `workflow` and `key-files` above, already narrated by
    # the default voice; these two are the back half and match it deliberately.
    # The sequence lives on the pages, not in the cuts — no "3 of 4" chrome and
    # no next-up endings, so each one is still safe to embed on its own.
    dict(name="locale-store", dir=r"shared\tutorial\locale-store", secs=32,
         groups=[2, 2, 2],
         starts=[2, 7, 12, 16.5, 21.5, 26.5],
         lines=[
             "Everything reactive in Langsys hangs off one small piece of state, the current locale.",
             "You hand that store to init just once, and from then on the SDK watches it.",

             "Write one of your project's target locales into it, and the whole tree re-renders.",
             "And it is your own framework's reactive primitive, a writable, a ref, or a signal.",

             "Each switch fetches that locale's catalog once, and the text on screen holds until it lands.",
             "Which is exactly how a single switcher can drive React, Vue and Svelte all at the same time.",
         ]),
    # The load-bearing claim is capability, not policy — the key you ship is
    # safe in a public bundle because from a visitor's address it physically
    # cannot write. Beat 4 has to say that, not merely assert shipping is fine.
    #
    # This is the low-level companion to the explainer's discovery story:
    # three key types (ip_write is the one a public site ships — read-only to
    # the world, write from addresses it trusts, and the renderer's address is
    # trusted by default), the two answers on startup, the two lanes the SDK
    # chooses between, the hint request itself, Langsys's visit, and the
    # callback. Capability is per SESSION and permission is per KEY; the spec
    # insists they are never collapsed, so the narration keeps "this session"
    # and "this key" apart on purpose.
    # Rebuilt from the ground up on the explainer's 09:00 blog post. The old
    # cut opened on "three key types" as a fact; this one opens on the reason
    # types exist (a key that can register can spend your budget), lets the
    # read-only key be a dead end, and only then introduces ip-write — as one
    # key whose answer depends on where you ask from. Beats 5-10 are the same
    # article at wire level, and beat 11 is the "ip" in ip-write.
    dict(name="keys-and-environments", dir=r"shared\tutorial\keys-and-environments", secs=86.75,
         groups=[3, 3, 2, 2, 2, 1, 1],
         starts=[2, 8, 13.5, 19.5, 26.5, 33.5, 39, 45, 50.75, 56.25, 62.25, 67.75, 73.25, 79],
         lines=[
             "A key that can register phrases can spend your machine-translation budget, so it must never ship in a bundle.",
             "A read-only key is safe to ship, but then nothing new on that site ever registers itself.",
             "So there is a third key, ip-write, which writes only from the IP addresses you list, and reads from anywhere.",

             "When you create the key, list the addresses your team browses from, and anyone browsing there registers new content on the spot.",
             "In short, write keys stay on your machines, ip-write goes in any public site, and read-only is for bundles that never change.",
             "So you build with the write key on your machine, and ship the ip-write key to production.",

             "Now watch it work — at nine a writer publishes an article, on a page no developer ever opens.",
             "Then the reader's browser asks two questions, can I write from here, and may I report what I see.",

             "It cannot write from here, so it sends Langsys the page's address, once, and never the text.",
             "Langsys checks the page is on your registered site, then opens it in a headless browser from its own address.",

             "Your key trusts that address, so the same SDK can now write, and registers the page.",
             "The phrases are machine-translated on arrival, and the next reader gets them in Spanish.",

             "So anyone on an address you trust registers directly, and the renderer covers the rest.",

             "And every key points at one project, holding your base locale and every target you added.",
         ]),

    # hero used to be a 13s montage whose beats ran as short as 0.8s, which is
    # under the time it takes to read the caption -- so the narration was three
    # coarse windows spanning several cuts each, and the picture went unnarrated
    # in between. At 28s the beats are 3-5s and every one of them carries its own
    # line, in three grouped breaths: the problem, the locale work, the payoff.
    # groups: the problem, the deletion and the payoff are each read alone.
    # They used to sit in one group of two, so the pivot from someone else's
    # library to Langsys happened inside a single breath with no pause on it --
    # audio-only, the only marker was the word "instead".
    # Rebuilt as a from-scratch explanation. The old cut gave the pivot 2.0s,
    # put name_gender on screen two beats before anything explained it, and
    # went straight from flat Spanish to the gendered version — so the branch
    # answered a question the viewer had never been asked. Spanish is now
    # allowed to be wrong for Laura first, and ICU select is said in words.
    dict(name="hero", dir=r"svelte\web\hero", secs=56.5,
         groups=[3, 2, 2, 2, 2],
         starts=[2, 6.5, 12, 18.25, 22.5, 26.75, 31.25, 35.5, 40.25, 45.25, 49.25],
         lines=[
             "Any other i18n library makes every string a key that points at a file.",
             "None of that is the translation, it is a label you made up and a cabinet to file the sentence in.",
             "So Langsys takes it away, and no translated word goes with it, because there never was one in there.",

             "You write the sentence instead, and that sentence itself becomes the key.",
             "Switch to Spanish, and the very same line comes back translated.",

             "But Spanish greets a man and a woman differently, so this is wrong for Laura.",
             "So you pass the gender your app already holds, on that same call.",

             "The Spanish entry then carries all three wordings, and your code carries none.",
             "Bienvenida for Laura, Bienvenido for Diego, decided as the page renders.",

             "And when nothing on the record says, the third wording answers instead.",
             "Every locale after that comes from the very same line you already wrote.",
         ]),
]

LEAD = 0.12          # beat of air after each cut before the line starts
VO_GAIN = 0.72
DUCK_TO = 0.45       # sting level once narration begins


# ── helpers ─────────────────────────────────────────────────────────────────

def read_wav(path):
    with wave.open(path, 'rb') as w:
        sr, ch, n = w.getframerate(), w.getnchannels(), w.getnframes()
        x = np.frombuffer(w.readframes(n), dtype='<i2').astype(np.float64) / 32768.0
    if ch > 1:
        x = x.reshape(-1, ch)
    return x, sr


def trim(x, thresh=0.01):
    loud = np.abs(x) > thresh
    if not loud.any():
        return x
    a = int(np.argmax(loud))
    b = len(loud) - int(np.argmax(loud[::-1]))
    return x[a:b]


def clean(x):
    """Neural voices arrive already mixed — a gentle high-pass and light
    limiting only. Anything heavier makes them worse."""
    b, a = signal.butter(2, 80 / (SR / 2), 'high')
    x = signal.lfilter(b, a, x)
    m = np.max(np.abs(x))
    if m > 0:
        x = x / m
    return np.tanh(x * 1.05) / np.tanh(1.05)


def fades(x, fi=0.012, fo=0.05):
    ni, no = min(int(fi * SR), len(x) // 2), min(int(fo * SR), len(x) // 2)
    if ni:
        x[:ni] *= np.linspace(0, 1, ni)
    if no:
        x[-no:] *= np.linspace(1, 0, no)
    return x


async def synth_group(texts, voice, out_mp3, rate=RATE):
    """Synthesize consecutive lines as ONE utterance.

    Synthesizing line by line is what made the early narration sound like
    someone reading a list: every line got a fresh start and a full
    sentence-final fall, then sat in a block of dead air until the next beat.
    Sent together, the voice carries intonation across the whole run and the
    pauses between sentences are its own.

    Returns each sentence's (start, duration) inside the rendered audio, taken
    from the service's SentenceBoundary events, so a continuous read can still
    be checked line-by-line against the picture it is describing.
    """
    joined = spoken(' '.join(t.strip() for t in texts))
    audio, bounds = bytearray(), []
    async for ch in edge_tts.Communicate(joined, voice, rate=rate).stream():
        if ch['type'] == 'audio':
            audio.extend(ch['data'])
        elif ch['type'] == 'SentenceBoundary':
            bounds.append((ch['offset'] / 1e7, ch['duration'] / 1e7))
    with open(out_mp3, 'wb') as fh:
        fh.write(audio)

    # One sentence per line is the contract that makes the mapping back to
    # beats unambiguous. A line carrying a second full stop would silently
    # shift every line after it onto the wrong picture.
    # This fires spuriously now and then: the service occasionally returns fewer
    # SentenceBoundary events than the text has sentences, and the identical
    # group builds cleanly on a retry. Re-run once before going hunting for a
    # stray full stop.
    if len(bounds) != len(texts):
        raise AssertionError(
            f"{len(texts)} lines produced {len(bounds)} sentences — keep one "
            f"sentence per line (commas and dashes are fine, full stops are not):"
            f"\n  " + "\n  ".join(texts))
    return bounds


def run(args):
    return subprocess.run(args, capture_output=True)


# ── per demo ────────────────────────────────────────────────────────────────

async def build(demo):
    name, ddir, secs = demo["name"], demo["dir"], demo["secs"]
    starts, lines = demo["starts"], demo["lines"]
    voice = demo.get("voice", VOICE)
    rate = demo.get("rate", RATE)
    total = INTRO_LEN + secs
    N = int(SR * total)

    assert len(starts) == len(lines), \
        f"{name}: {len(starts)} scene starts but {len(lines)} lines"

    # A line left hanging on a comma is read as one sentence with the line after
    # it, which collapses two beats into one and slides the rest of the group
    # onto the wrong pictures. Tempting for flow, and silently wrong — carry the
    # thought with the wording instead ("And ...", "So ..."), not the comma.
    for i, ln in enumerate(lines):
        assert ln.rstrip().endswith(('.', '!', '?')), \
            f"{name} line {i+1} must be a complete sentence: {ln!r}"

    # Without this the concat silently produces nothing and the mux leaves the
    # previous mp4 in place, which looks exactly like a successful no-op run.
    demo_mp4 = os.path.join(BASE, f"body-{name}.mp4")
    if not os.path.exists(demo_mp4):
        print(f"\n=== {name}  SKIPPED — no {demo_mp4}")
        return 0

    vo_dir = os.path.join(BASE, "vo-" + name)
    os.makedirs(vo_dir, exist_ok=True)

    print(f"\n=== {name}  ({total:.1f}s total, {voice})")

    bed = np.zeros((N, 2))
    sting, sr_s = read_wav(INTRO_WAV)
    if sr_s != SR:
        sting = signal.resample_poly(sting, SR, sr_s)
    bed[:min(len(sting), N)] += sting[:N]

    vo = np.zeros(N)
    problems = 0

    # Group sizes: how many consecutive lines are read as one breath. Absent,
    # every line is its own group, which is the old line-at-a-time behaviour.
    sizes = demo.get("groups") or [1] * len(lines)
    assert sum(sizes) == len(lines), \
        f"{name}: groups sum to {sum(sizes)} but there are {len(lines)} lines"

    first = 0
    for g, size in enumerate(sizes):
        members = list(range(first, first + size))
        first += size

        mp3 = os.path.join(vo_dir, f"g{g}.mp3")
        wav = os.path.join(vo_dir, f"g{g}.wav")
        bounds = await synth_group([lines[i] for i in members], voice, mp3, rate)
        run([FF, "-y", "-i", mp3, "-ar", str(SR), "-ac", "1", wav])

        x, sr0 = read_wav(wav)
        if x.ndim > 1:
            x = x.mean(axis=1)
        if sr0 != SR:
            x = signal.resample_poly(x, SR, sr0)
        # No trim() here — the offsets are measured against the untrimmed
        # render, so cutting leading silence would slide every line early.
        x = fades(clean(x))

        # Anchor the group so its first sentence's speech starts on that beat.
        # Later lines fall where the read puts them; the group re-anchors, so
        # drift can never accumulate past the end of one group.
        head = bounds[0][0]
        t0 = INTRO_LEN + starts[members[0]] + LEAD
        a = int((t0 - head) * SR)
        b = min(max(a, 0) + len(x), N)
        src = x[max(0, -a):]
        a = max(a, 0)
        if b > a:
            vo[a:b] += src[:b - a] * VO_GAIN

        for k, i in enumerate(members):
            s = t0 + (bounds[k][0] - head)
            e = s + bounds[k][1]
            win0 = INTRO_LEN + starts[i]
            win1 = INTRO_LEN + (starts[i + 1] if i + 1 < len(starts) else secs)
            fill = bounds[k][1] / (win1 - win0) * 100

            # In a continuous read there is no long pause to absorb a mistimed
            # line: one written short pulls every line after it early, onto the
            # picture before its own. Both directions are errors, so a line's
            # spoken length has to match its beat, not just fit inside it.
            early = s < win0 - 0.45         # speaking over the previous picture
            late = s > win1 - 0.05          # started after its picture is gone
            over = e > win1 + 0.35          # ran into the next picture
            if early or late or over:
                problems += 1
            flag = ('STARTS EARLY by %.2fs' % (win0 - s) if early
                    else 'STARTS LATE' if late
                    else 'OVERRUNS by %.2fs' % (e - win1) if over else 'ok')
            print(f"   {i+1:2}  {s:6.2f} -> {e:6.2f}   beat {win0:6.2f}-{win1:6.2f}"
                  f"   fill {fill:3.0f}%   {flag}")

    # Duck the sting once narration starts so the choir sits under the voice.
    duck = np.ones(N)
    d0 = int((INTRO_LEN - 0.10) * SR)
    d1 = int((INTRO_LEN + 0.45) * SR)
    duck[d0:d1] = np.linspace(1.0, DUCK_TO, d1 - d0)
    duck[d1:] = DUCK_TO
    bed *= duck[:, None]

    out = bed + np.stack([vo, vo], axis=1) * 0.95
    tail = int(0.08 * SR)
    out[-tail:] *= np.linspace(1, 0, tail)[:, None]
    peak = np.max(np.abs(out))
    if peak > 0:
        out *= 10 ** (-1.5 / 20) / peak

    bed_wav = os.path.join(BASE, f"bed-{name}.wav")
    with wave.open(bed_wav, 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((np.clip(out, -1, 1) * 32767).astype('<i2').tobytes())

    # ── video: strip the intro's own audio, concat, mux the new bed ─────────
    # The sting holds a static, full-brightness logo for its last ~1.6s and then
    # stops dead, so the concat below cut from that straight into the demo's
    # first frame. Fading the tail turns the join into a dip: the master fades
    # back up out of the same black on its own side. Re-encoded, not copied —
    # hence a new filename, so a cached intro-novo.mp4 from before this change
    # is not silently reused.
    intro_v = os.path.join(BASE, "intro-novo-fade.mp4")
    if not os.path.exists(intro_v):
        run([FF, "-y", "-i", INTRO_MP4, "-an",
             "-vf", f"fade=t=out:st={INTRO_LEN - 0.30:.2f}:d=0.30",
             "-c:v", "libx264", "-preset", "slow", "-crf", "18",
             "-pix_fmt", "yuv420p", "-r", "30", intro_v])

    listf = os.path.join(BASE, f"concat-{name}.txt")
    with open(listf, "w") as fh:
        fh.write(f"file '{intro_v}'\n".replace("\\", "/"))
        fh.write(f"file '{demo_mp4}'\n".replace("\\", "/"))

    combined = os.path.join(BASE, f"combined-{name}.mp4")
    run([FF, "-y", "-f", "concat", "-safe", "0", "-i", listf, "-c", "copy", combined])

    final = os.path.join(REPO, ddir, name + ".mp4")
    run([FF, "-y", "-i", combined, "-i", bed_wav,
         "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", str(SR), "-ac", "2",
         "-shortest", "-movflags", "+faststart", final])

    print(f"   -> {ddir}\\{name}.mp4   ({problems} overrun{'' if problems == 1 else 's'})")
    return problems


async def main():
    import sys
    only = sys.argv[1] if len(sys.argv) > 1 else None
    bad = 0
    for d in DEMOS:
        if only and d['name'] != only:
            continue
        bad += await build(d)
    print(f"\n=== finished. {bad} line(s) overrunning their beat.")

if __name__ == "__main__":
    asyncio.run(main())
