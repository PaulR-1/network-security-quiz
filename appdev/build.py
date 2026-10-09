#!/usr/bin/env python3
"""Generate the ICS26011 application-development quizzes from the reviewer notes."""

import json
from pathlib import Path

OUT = Path(__file__).resolve().parent


def single(q, right, wrongs, explain, source):
    options = [right[0]] + [w[0] for w in wrongs]
    why = {right[0]: right[1]}
    why.update({t: w for t, w in wrongs})
    return {
        "type": "single",
        "q": q,
        "options": options,
        "answer": [right[0]],
        "why": why,
        "explain": explain,
        "source": source,
    }


def multi(q, rights, wrongs, explain, source):
    n = len(rights)
    text = q if "(Select " in q else f"{q} (Select {n})"
    options = [t for t, _ in rights] + [t for t, _ in wrongs]
    why = {t: w for t, w in rights + wrongs}
    return {
        "type": "multi",
        "q": text,
        "options": options,
        "answer": [t for t, _ in rights],
        "why": why,
        "explain": explain,
        "source": source,
    }


def match(q, rows, choices, explain, source, hint="Match each item."):
    return {
        "type": "match",
        "q": q,
        "hint": hint,
        "items": [item for item, _ in rows],
        "choices": [{"v": v, "l": label} for v, label in choices],
        "map": {item: v for item, v in rows},
        "explain": explain,
        "source": source,
    }


def module1():
    return [
        single(
            "What is mobile application development?",
            ("Developing applications for mobile devices such as PDAs, enterprise digital assistants, and mobile phones",
             "The module defines it as that act or process, and it names those devices."),
            [
                ("Writing firmware for network routers",
                 "The definition is about applications for mobile devices, not router firmware."),
                ("Designing only the Linux kernel",
                 "Android is Linux-based, but this definition is about building mobile applications."),
                ("Publishing desktop-only programs",
                 "The definition names mobile devices, not desktop-only programs."),
            ],
            "It is the process of building applications for mobile devices such as PDAs, enterprise digital assistants, and phones.",
            "Module 1, Mobile Application Development",
        ),
        single(
            "How does the module present Android?",
            ("An open-source, Linux-based operating system for smartphones and tablets",
             "That is the module's description: open-source, Linux-based, for smartphones and tablet computers."),
            [
                ("A closed-source desktop operating system",
                 "The module calls Android open-source and Linux-based, for phones and tablets."),
                ("A programming language that replaced Kotlin",
                 "Kotlin is a language used to write Android apps. Android is the operating system."),
                ("The Google Play billing service",
                 "Google Play is the distribution ecosystem. Android is the operating system."),
            ],
            "Android is an open-source, Linux-based operating system for smartphones and tablets.",
            "Module 1, What is Android?",
        ),
        multi(
            "Android applications are primarily written in which languages?",
            [
                ("Java", "The module says Android applications are primarily written in Java."),
                ("Kotlin", "The same point says they are increasingly written in Kotlin."),
            ],
            [
                ("XML layouts", "XML defines the visual interface. It is not named as the language apps are primarily written in."),
                ("The Layout Editor", "The Layout Editor is a tool for building the UI, not a language."),
            ],
            "The module says Android apps are primarily written in Java and, increasingly, Kotlin.",
            "Module 1, What is Android?",
        ),
        single(
            "Where does the module center Android's app ecosystem?",
            ("Google Play",
             "The introduction says Android is distributed through an ecosystem centered on Google Play."),
            [
                ("The Apple App Store",
                 "The module centers Android distribution on Google Play."),
                ("Only files copied between phones, with no store",
                 "The module describes a store ecosystem centered on Google Play."),
                ("Android Market, as the name of the current ecosystem",
                 "Android Market is listed under Android 1.0. The introduction centers the ecosystem on Google Play."),
            ],
            "Distribution is an app ecosystem centered on Google Play.",
            "Module 1, What is Android?",
        ),
        single(
            "Why does the module say Android is worth learning?",
            ("It has a large number of users and applications, so it is a major platform",
             "The Why Android section points to that large user and application base."),
            [
                ("It has the smallest mobile user base",
                 "The module uses the large user base as the reason, not a small one."),
                ("It runs on only one phone model",
                 "The module stresses how widely Android is used, including devices beyond phones."),
                ("It is the language that replaced Kotlin",
                 "Kotlin is a way to write Android apps. The reason to learn Android is the size of the platform."),
            ],
            "The module points to Android's large number of users and applications.",
            "Module 1, Why Android?",
        ),
        single(
            "When and where was Android Inc. founded?",
            ("October 2003, in Palo Alto, California",
             "The Android Story slides give October 2003 and Palo Alto."),
            [
                ("January 2008, in Mountain View",
                 "The slides place the founding in Palo Alto in October 2003."),
                ("October 2005, in Seattle",
                 "The year in the slides is 2003, and the city is Palo Alto."),
                ("March 2010, in Austin",
                 "The founding in the module is October 2003 in Palo Alto."),
            ],
            "Android Inc. was founded in Palo Alto, California, in October 2003.",
            "Module 1, The Android Story",
        ),
        single(
            "Who does the module name as the founders of Android Inc.?",
            ("Andy Rubin, Rich Miner, Nick Sears, and Chris White",
             "The Android Story names those four founders."),
            [
                ("Andy Rubin alone",
                 "Andy Rubin is one founder. The slides also name Rich Miner, Nick Sears, and Chris White."),
                ("Rich Miner and Nick Sears only",
                 "Those two are founders, and the slides also name Andy Rubin and Chris White."),
                ("Chris White only",
                 "Chris White is one of the four. The full list is Rubin, Miner, Sears, and White."),
            ],
            "Android Inc. was founded by Andy Rubin, Rich Miner, Nick Sears, and Chris White.",
            "Module 1, The Android Story",
        ),
        single(
            "What original goal does the Android Story give?",
            ("A smarter mobile device that was more aware of its owner's location and preferences",
             "That is the original goal written in the slides."),
            [
                ("A desktop operating system meant to replace Windows",
                 "The goal in the slides is a smarter mobile device, not a desktop OS."),
                ("A closed store that blocked third-party apps",
                 "The slides describe location and preference awareness, not a closed store."),
                ("The tablet-only Honeycomb interface",
                 "Honeycomb is a later tablet release. The original goal was a smarter device aware of location and preferences."),
            ],
            "The original goal was a smarter mobile device, more aware of its owner's location and preferences.",
            "Module 1, The Android Story",
        ),
        match(
            "Match each Android platform with what the module says it is for.",
            [
                ("Android TV", "tv"),
                ("Android Auto", "auto"),
                ("Wear OS / Android Wear", "wear"),
                ("Android-powered appliances", "appliances"),
            ],
            [
                ("tv", "Digital media players"),
                ("auto", "Compatible car displays"),
                ("wear", "Smartwatches and wearables"),
                ("appliances", "Tablets, cameras, microwaves, washers"),
            ],
            "TV is for media players, Auto for car displays, Wear OS for wearables, and the module also shows Android on appliances.",
            "Module 1, Android Beyond Smartphones",
            "Choose the platform the description belongs to.",
        ),
        single(
            "What does the module say Android TV emphasizes?",
            ("Content discovery and voice search, with Assistant and Cast",
             "The Android TV row names content discovery, voice search, Assistant, and Cast."),
            [
                ("Fingerprint unlock and USB-C",
                 "Fingerprint support and USB-C are Marshmallow points, not the Android TV description."),
                ("Picture-in-picture and notification channels",
                 "Those are Oreo points. Android TV emphasizes content discovery, voice search, Assistant, and Cast."),
                ("Watch-face styles and 3G/LTE",
                 "Watch faces, Bluetooth, Wi-Fi, and 3G/LTE are in the Wear OS row."),
            ],
            "Android TV emphasizes content discovery and voice search, and it integrates Assistant and Cast.",
            "Module 1, Android TV",
        ),
        single(
            "Why does the module encourage voice control in Android Auto?",
            ("For safer operation while using the car display",
             "The Auto row says voice control is encouraged for safer operation."),
            [
                ("So the driver has to watch the screen more closely",
                 "The module encourages voice control for safer operation, not more screen watching."),
                ("Because Auto is the smartwatch operating system",
                 "Smartwatches are Wear OS. Android Auto is for compatible car displays."),
                ("To install apps onto an SD card",
                 "SD-card installation is an Android 2.2 Froyo point, not the reason for Auto voice control."),
            ],
            "Voice control in Android Auto is encouraged for safer operation.",
            "Module 1, Android Auto",
        ),
        single(
            "What does the module associate with Wear OS / Android Wear?",
            ("Smartwatches, notifications, Assistant, Bluetooth, Wi-Fi, 3G/LTE, and watch-face styles",
             "That list is the Wear OS row in the slides."),
            [
                ("Car navigation, music, SMS, and telephone",
                 "Those examples belong to Android Auto."),
                ("Content discovery on a digital media player",
                 "That is the Android TV description."),
                ("Microwaves and washing machines only",
                 "Appliances are a separate row. Wear OS is the watch and wearable system."),
            ],
            "Wear OS is the Android-based system for smartwatches and other wearables, including notifications, Assistant, radios, and watch faces.",
            "Module 1, Wear OS",
        ),
        single(
            "Which code name does Android 1.0 have in the module?",
            ("No specific code name",
             "The version table leaves 1.0 with no specific code name."),
            [
                ("Cupcake", "Cupcake is Android 1.5."),
                ("Donut", "Donut is Android 1.6."),
                ("Eclair", "Eclair is Android 2.0/2.1."),
            ],
            "Android 1.0 is listed with no specific code name.",
            "Module 1, Android 1.0",
        ),
        match(
            "Match each early Android version with its code name.",
            [
                ("1.5", "cupcake"),
                ("1.6", "donut"),
                ("2.0/2.1", "eclair"),
                ("2.2", "froyo"),
                ("2.3", "gingerbread"),
                ("3.0/3.1/3.2", "honeycomb"),
                ("4.0", "ics"),
                ("4.1/4.2/4.3", "jellybean"),
                ("4.4", "kitkat"),
            ],
            [
                ("cupcake", "Cupcake"),
                ("donut", "Donut"),
                ("eclair", "Eclair"),
                ("froyo", "Froyo"),
                ("gingerbread", "Gingerbread"),
                ("honeycomb", "Honeycomb"),
                ("ics", "Ice Cream Sandwich"),
                ("jellybean", "Jelly Bean"),
                ("kitkat", "KitKat"),
            ],
            "1.5 Cupcake through 4.4 KitKat follow the version table. Android 1.0 has no code name.",
            "Module 1, versions 1.5–4.4",
            "Pick the code name for each version.",
        ),
        match(
            "Match each later Android version with its code name from the slides.",
            [
                ("5.0/5.1", "lollipop"),
                ("6.0", "marshmallow"),
                ("7.0", "nougat"),
                ("8.0", "oreo"),
                ("9.0", "pie"),
                ("10", "quince"),
                ("11", "redvelvet"),
                ("12/12L", "snow"),
                ("14", "upside"),
                ("15", "vanilla"),
            ],
            [
                ("lollipop", "Lollipop"),
                ("marshmallow", "Marshmallow"),
                ("nougat", "Nougat"),
                ("oreo", "Oreo"),
                ("pie", "Pie"),
                ("quince", "Quince Tart"),
                ("redvelvet", "Red Velvet Cake"),
                ("snow", "Snow Cone"),
                ("upside", "Upside Down Cake"),
                ("vanilla", "Vanilla Ice Cream"),
            ],
            "The later table runs from Lollipop through Vanilla Ice Cream. The slides do not list a version 13.",
            "Module 1, versions 5–15",
            "Pick the code name for each version.",
        ),
        match(
            "Match each early feature set with the version that presents it.",
            [
                ("Gmail, Calendar, Maps, pull-down notifications, and Android Market", "v10"),
                ("Animated transitions, YouTube uploads, widgets, and the on-screen keyboard", "cupcake"),
                ("Voice search, handwriting gestures, and 800×480 support", "donut"),
                ("Speech-to-text, multiple accounts, and pinch-to-zoom", "eclair"),
                ("SD-card app installation, USB tethering, and Wi-Fi hotspot", "froyo"),
                ("NFC and Google Wallet on the Nexus S 4G", "ginger"),
                ("Tablet-focused release with hardware acceleration", "honey"),
                ("Face Unlock and virtual buttons", "ics"),
                ("Native emoji, group messaging, and a smoother UI", "jelly"),
                ("“Ok, Google”, a printing framework, and translucent UI", "kitkat"),
            ],
            [
                ("v10", "1.0"),
                ("cupcake", "Cupcake"),
                ("donut", "Donut"),
                ("eclair", "Eclair"),
                ("froyo", "Froyo"),
                ("ginger", "Gingerbread"),
                ("honey", "Honeycomb"),
                ("ics", "Ice Cream Sandwich"),
                ("jelly", "Jelly Bean"),
                ("kitkat", "KitKat"),
            ],
            "Each row is the major-points cell for that version in the Module 1 table.",
            "Module 1, features 1.0–KitKat",
            "Pick the version for each feature set.",
        ),
        match(
            "Match each later feature set with the version that presents it.",
            [
                ("High-performance graphics, screen capture and sharing, and a card-based concept", "lollipop"),
                ("Fingerprint support and USB-C", "marsh"),
                ("Multi-window, Direct Boot, Data Saver, and Google Assistant", "nougat"),
                ("Picture-in-picture, notification channels, and background execution limits", "oreo"),
                ("Digital Wellbeing and hybrid gesture/button navigation", "pie"),
                ("System-wide dark theme, Focus Mode, Live Caption, and granular location permissions", "ten"),
                ("Limited single-use permissions for location, camera, and microphone", "eleven"),
                ("Material You and dynamic theming from wallpaper colors", "twelve"),
                ("Cross-app text drag and drop, lock-screen customization, and AI-generated wallpaper", "fourteen"),
                ("Listed in the module as Android 15.0", "fifteen"),
            ],
            [
                ("lollipop", "Lollipop"),
                ("marsh", "Marshmallow"),
                ("nougat", "Nougat"),
                ("oreo", "Oreo"),
                ("pie", "Pie"),
                ("ten", "Android 10"),
                ("eleven", "Android 11"),
                ("twelve", "Android 12"),
                ("fourteen", "Android 14"),
                ("fifteen", "Android 15"),
            ],
            "These are the major points in the later version table, including the Android 15.0 line.",
            "Module 1, features Lollipop–15",
            "Pick the version for each feature set.",
        ),
        single(
            "Which version is presented as the first without a dessert-themed public name?",
            ("Android 10",
             "The Android 10 row says it is the first version presented without a dessert-themed public name. The table still lists Quince Tart in the code-name column."),
            [
                ("Android 9 Pie", "Pie is the dessert name on Android 9.0."),
                ("Android 4.4 KitKat", "KitKat is the dessert name for Android 4.4."),
                ("Android 15 Vanilla Ice Cream",
                 "Android 15 is listed as Vanilla Ice Cream. The no-public-dessert-name point is made about Android 10."),
            ],
            "Android 10 is called the first version without a dessert-themed public name, even though the table lists Quince Tart.",
            "Module 1, Android 10",
        ),
        single(
            "Which development environment does the module use for Android apps?",
            ("Android Studio",
             "Getting Started names Android Studio as the development environment."),
            [
                ("Google Play", "Google Play distributes apps. Android Studio is where the module builds them."),
                ("The Layout Editor alone, treated as the whole IDE",
                 "The Layout Editor is one part of Android Studio. The module names Android Studio as the environment."),
                ("The phone Settings screen",
                 "A test device runs the app. The development environment is Android Studio."),
            ],
            "Android Studio is the development environment used in the module.",
            "Module 1, Getting Started",
        ),
        single(
            "Where does the module send students to install Android Studio?",
            ("The official Android Studio site",
             "The module directs students to the official Android Studio site for installation and setup."),
            [
                ("The Android 1.0 Market download list",
                 "Android Market is a 1.0 feature. Installation is directed to the official Android Studio site."),
                ("A Wear OS watch face",
                 "Watch faces are a Wear OS topic. Studio is installed from its official site."),
                ("The Status bar inside a project that is already open",
                 "The Status bar reports IDE status. It is not the installation source."),
            ],
            "Installation and setup are directed to the official Android Studio site.",
            "Module 1, Getting Started",
        ),
        single(
            "What does the module use to run and test an application?",
            ("A test device or a simulator/emulator",
             "Getting Started says a test device or simulator/emulator is used to run and test applications."),
            [
                ("Only the version-control tool window",
                 "Version control is one tool window. Running the app uses a test device or emulator."),
                ("Google Play, before the project exists",
                 "The workflow runs the app on a test device. Play is the distribution ecosystem."),
                ("The printing framework from KitKat",
                 "Printing is a KitKat feature, not how this module runs a student project."),
            ],
            "Apps are run and tested on a test device or a simulator/emulator.",
            "Module 1, Getting Started",
        ),
        single(
            "Which development workflow does the module introduce?",
            ("Create an Android project, edit the UI and Kotlin, then run it on a test device",
             "That is the workflow order in Getting Started."),
            [
                ("Publish on Google Play, then create the project",
                 "The module starts by creating the project, then editing, then running on a test device."),
                ("Write only XML, skip Kotlin, and never run the app",
                 "The workflow includes editing both the UI and the Kotlin code, then running the app."),
                ("Call onDestroy, then create the project",
                 "onDestroy is a lifecycle callback. It is not the start of the development workflow."),
            ],
            "The workflow is: create a project, edit the UI and Kotlin, then run the app on a test device.",
            "Module 1, Getting Started",
        ),
        match(
            "Match each Android Studio area with its job.",
            [
                ("Toolbar", "toolbar"),
                ("Navigation bar", "nav"),
                ("Editor window", "editor"),
                ("Tool window bar", "bar"),
                ("Tool windows", "tools"),
                ("Status bar", "status"),
            ],
            [
                ("toolbar", "Run the app and launch tools"),
                ("nav", "Open files; compact project view"),
                ("editor", "Create and modify code"),
                ("bar", "Expand or collapse tool windows"),
                ("tools", "Project, search, version control"),
                ("status", "Status, warnings, and messages"),
            ],
            "Toolbar runs the app, the navigation bar opens files, the editor edits, tool windows hold tasks, and the status bar shows warnings.",
            "Module 1, Android Studio User Interface",
            "Pick the job of each area.",
        ),
    ]


def module2():
    return [
        single(
            "How does Module 2 introduce Kotlin?",
            ("As the language for the course, learned by building a basic app and running it on an emulator",
             "The module introduces Kotlin as the mobile language and follows a learning-by-doing path onto an emulator."),
            [
                ("As a replacement for XML layouts, with no emulator step",
                 "XML still describes the interface. The module has you build an app and run it on an emulator."),
                ("As the Android operating system itself",
                 "Android is the operating system. Kotlin is the language the module uses to write the app."),
                ("As a dessert code name for Android 4.4",
                 "KitKat is the 4.4 code name. Kotlin is the programming language in this module."),
            ],
            "Module 2 uses Kotlin and has you learn it by building a basic app and running it on an emulator.",
            "Module 2, Kotlin",
        ),
        single(
            "What does the module say the Android project structure contains?",
            ("Package name, Activity names, the main Activity, version support, hardware features, and permissions",
             "That is the configuration list in the project-structure section."),
            [
                ("Only watch-face styles and Android TV search",
                 "Those are platform topics. The project structure holds package, Activity, version, hardware, and permission information."),
                ("Digital Wellbeing, Focus Mode, and Live Caption",
                 "Those are later Android version features, not the project-structure list."),
                ("Lifecycle callbacks and no permission information",
                 "The list includes permissions, the main Activity, version support, and hardware features."),
            ],
            "The project holds the package name, Activity names, entry Activity, version and hardware support, permissions, and related configuration.",
            "Module 2, project structure",
        ),
        single(
            "What is the Layout Editor?",
            ("The Android Studio environment for creating and editing the visual user interface",
             "That is the module's definition of the Layout Editor."),
            [
                ("The window that only shows Git history",
                 "Version control is a tool window. The Layout Editor edits the visual UI."),
                ("The callback Android runs when the Activity is destroyed",
                 "That is onDestroy. The Layout Editor edits the interface."),
                ("The store centered on Google Play",
                 "Google Play distributes apps. The Layout Editor builds the visual UI in Android Studio."),
            ],
            "The Layout Editor is where you create and edit the application's visual user interface.",
            "Module 2, Layout Editor",
        ),
        multi(
            "Which of these are input controls listed in the module?",
            [
                ("Buttons", "Buttons are in the module's list of input controls."),
                ("SeekBars", "SeekBars are in the module's list of input controls."),
                ("CheckBoxes", "CheckBoxes are in the module's list of input controls."),
                ("ToggleButtons", "ToggleButtons are in the module's list of input controls."),
            ],
            [
                ("onDestroy()", "onDestroy is a lifecycle callback, not an input control."),
                ("Google Play", "Google Play is the distribution ecosystem, not a UI input control."),
            ],
            "Input controls are interactive UI components. The list includes Buttons, text fields, SeekBars, CheckBoxes, zoom buttons, and ToggleButtons.",
            "Module 2, UI Controls",
        ),
        single(
            "What is a TextView in this module?",
            ("A control that displays text. The basic configuration is not editable, though the underlying class can edit text",
             "The module says a TextView displays text, and that the basic configuration is not editable while the class itself is capable of text editing."),
            [
                ("An editable field whose basic job is rich text entry",
                 "That description is EditText, the editable subclass of TextView."),
                ("A push-button that performs an action",
                 "That is a Button."),
                ("A container that scrolls vertically",
                 "That is a ScrollView, not a TextView."),
            ],
            "A TextView displays text. Its basic configuration is not editable, even though the underlying class can edit text.",
            "Module 2, TextView",
        ),
        match(
            "Match each TextView attribute with what the module says it does.",
            [
                ("Uniquely identifies the control", "id"),
                ("Text to display", "text"),
                ("Automatically capitalizes user-entered text", "cap"),
                ("Specifies the font family", "font"),
                ("Controls text size", "size"),
                ("Sets bold, italic, or bold-italic", "style"),
                ("Aligns text inside the TextView", "gravity"),
                ("Limits how many lines are displayed", "lines"),
                ("Adds an ellipsis when text is wider than the view", "ellip"),
            ],
            [
                ("id", "android:id"),
                ("text", "android:text"),
                ("cap", "android:capitalize"),
                ("font", "android:fontFamily"),
                ("size", "android:textSize"),
                ("style", "android:textStyle"),
                ("gravity", "android:gravity"),
                ("lines", "android:maxLines"),
                ("ellip", "android:ellipsize"),
            ],
            "These are the TextView attributes in the module, from android:id through android:ellipsize.",
            "Module 2, TextView attributes",
            "Pick the attribute.",
        ),
        multi(
            "Which ellipsize positions does the module name?",
            [
                ("start", "start is one of the ellipsize options in the TextView table."),
                ("middle", "middle is one of the ellipsize options in the TextView table."),
                ("end", "end is one of the ellipsize options in the TextView table."),
            ],
            [
                ("match_parent", "match_parent is a layout width or height value, not an ellipsize position."),
            ],
            "android:ellipsize can use start, middle, or end when the text is wider than the view.",
            "Module 2, android:ellipsize",
        ),
        single(
            "What is an EditText?",
            ("An editable subclass of TextView with rich text-entry capabilities",
             "The module defines EditText as that editable subclass."),
            [
                ("A TextView configuration that cannot be edited at all",
                 "The basic TextView configuration is not editable. EditText is the editable subclass."),
                ("An image control loaded from a URI",
                 "That is an ImageView."),
                ("A card container with elevation",
                 "That is a CardView."),
            ],
            "EditText is an editable subclass of TextView for rich text entry.",
            "Module 2, EditText",
        ),
        single(
            "What is android:hint on an EditText?",
            ("Placeholder text shown when the field is empty",
             "The attribute table defines android:hint as the placeholder displayed when the field is empty."),
            [
                ("The unique id used from Kotlin",
                 "The identifier is android:id. android:hint is the empty-field placeholder."),
                ("The kind of data expected, such as a password",
                 "The expected data type is android:inputType."),
                ("A drawable drawn under the text",
                 "Drawables around the text use android:drawableLeft, Right, Top, or Bottom."),
            ],
            "android:hint is the placeholder shown while the EditText is empty.",
            "Module 2, android:hint",
        ),
        single(
            "What does android:autoText do?",
            ("Automatically corrects some common spelling errors",
             "The EditText table says android:autoText specifies input behavior with automatic correction of some common spelling errors."),
            [
                ("Capitalizes text the way android:capitalize does on a TextView",
                 "Capitalizing user-entered text is android:capitalize. autoText is the spelling-correction behavior."),
                ("Hides the field without removing its layout space",
                 "Hiding a view while keeping its space is the INVISIBLE visibility value."),
                ("Sets the font family",
                 "The font family is android:fontFamily."),
            ],
            "android:autoText turns on automatic correction of some common spelling errors.",
            "Module 2, android:autoText",
        ),
        single(
            "What does android:inputType specify?",
            ("The kind of data expected, such as text, number, or password",
             "That is the EditText table's definition, including those examples."),
            [
                ("Whether the text is bold, italic, or both",
                 "Bold and italic are android:textStyle."),
                ("How many lines the field may show",
                 "The line limit is android:maxLines."),
                ("The placeholder shown when the field is empty",
                 "The empty-field placeholder is android:hint."),
            ],
            "android:inputType sets the expected data, such as text, number, or password.",
            "Module 2, android:inputType",
        ),
        single(
            "What do android:drawableLeft, Right, Top, and Bottom do on an EditText?",
            ("Place a drawable relative to the entered or displayed text",
             "The EditText table says those attributes place a drawable relative to the text."),
            [
                ("Set the field's initial visibility",
                 "Initial visibility is android:visibility."),
                ("Choose text, number, or password input",
                 "That choice is android:inputType."),
                ("Tint the drawable of an ImageView",
                 "Image tint is android:tint. These drawable attributes sit around EditText text."),
            ],
            "Those attributes place a drawable to the left, right, top, or bottom of the text.",
            "Module 2, EditText drawables",
        ),
        single(
            "What is a Button in this module?",
            ("A push-button the user can press or click to perform an action",
             "That is the module's definition of a Button."),
            [
                ("A read-only text display",
                 "A read-only display is the basic TextView. A Button performs an action when pressed."),
                ("A two-dimensional grid of data",
                 "That is a GridView."),
                ("The Activity callback that runs when the screen is created",
                 "That is onCreate. A Button is a push-button control."),
            ],
            "A Button is a push-button the user presses to perform an action.",
            "Module 2, Button",
        ),
        single(
            "What is android:background on a Button?",
            ("The drawable used as the Button background",
             "The Button table defines android:background as that drawable."),
            [
                ("The text printed on the Button",
                 "The label is android:text."),
                ("The alignment of that text inside the Button",
                 "Alignment inside the Button is android:gravity."),
                ("The font family of the label",
                 "The font is android:fontFamily."),
            ],
            "android:background is the drawable used as the Button background.",
            "Module 2, Button attributes",
        ),
        single(
            "What does an ImageView display?",
            ("An image from resources or a URI, which can be scaled or cropped",
             "The module says an ImageView displays an image from resources or a URI and can scale or crop it."),
            [
                ("Only placeholder text for an empty field",
                 "Placeholder text is android:hint on an EditText."),
                ("A vertically scrolling column of widgets",
                 "Vertical scrolling is a ScrollView."),
                ("The IDE status and warnings",
                 "Status and warnings belong to the Android Studio status bar."),
            ],
            "An ImageView displays an image from resources or a URI, and the image can be scaled or cropped.",
            "Module 2, ImageView",
        ),
        single(
            "Which attribute sets an ImageView's image source?",
            ("android:src",
             "The ImageView table says android:src specifies the image source."),
            [
                ("android:hint", "android:hint is the empty EditText placeholder."),
                ("android:text", "android:text is the text shown on a text control or Button."),
                ("android:id", "android:id identifies the view. It does not choose the image."),
            ],
            "android:src specifies the ImageView's image source.",
            "Module 2, android:src",
        ),
        single(
            "What is android:contentDescription for?",
            ("Text for accessibility",
             "The ImageView table says android:contentDescription provides text for accessibility."),
            [
                ("A tint applied over the image",
                 "The tint is android:tint."),
                ("How the image is scaled, such as centerCrop",
                 "Scaling and positioning are android:scaleType."),
                ("The click handler in Kotlin",
                 "A click handler is setOnClickListener. contentDescription is accessibility text."),
            ],
            "android:contentDescription provides accessibility text for the ImageView.",
            "Module 2, android:contentDescription",
        ),
        single(
            "What does android:scaleType control?",
            ("How the image is resized and positioned, such as fitXY, centerCrop, and centerInside",
             "The module names android:scaleType for resizing and positioning and gives those examples."),
            [
                ("The accessibility text",
                 "Accessibility text is android:contentDescription."),
                ("A color tint over the image",
                 "The tint is android:tint."),
                ("Whether the ImageView is hidden",
                 "Visibility is android:visibility, not scaleType."),
            ],
            "android:scaleType controls how the image is resized and positioned. The module names fitXY, centerCrop, and centerInside.",
            "Module 2, android:scaleType",
        ),
        multi(
            "Which scaleType values does the module name?",
            [
                ("fitXY", "fitXY is one of the scaleType examples in the ImageView table."),
                ("centerCrop", "centerCrop is one of the scaleType examples in the ImageView table."),
                ("centerInside", "centerInside is one of the scaleType examples in the ImageView table."),
            ],
            [
                ("match_parent", "match_parent is a layout size value, not a scaleType name in this module."),
            ],
            "The named scaleType examples are fitXY, centerCrop, and centerInside.",
            "Module 2, scaleType values",
        ),
        single(
            "What is centerCrop, according to the quick review?",
            ("It fills the ImageView while preserving aspect ratio, and the excess may be cropped",
             "The quick review defines centerCrop that way."),
            [
                ("It shows the empty-field placeholder",
                 "The empty-field placeholder is android:hint."),
                ("It hides the view and frees its layout space",
                 "Hiding a view and freeing its space is GONE."),
                ("It sets the text size in scale-independent pixels",
                 "Text size uses sp. centerCrop is an ImageView scale type."),
            ],
            "centerCrop fills the ImageView, keeps the aspect ratio, and may crop the excess.",
            "Quick review, centerCrop",
        ),
        single(
            "What does android:tint do on an ImageView?",
            ("Applies a tint to the image",
             "The ImageView table says android:tint applies a tint to the image."),
            [
                ("Provides accessibility text",
                 "Accessibility text is android:contentDescription."),
                ("Chooses the image file or URI",
                 "The image source is android:src."),
                ("Limits the image to one line of text",
                 "android:maxLines limits text lines. It is not the image tint."),
            ],
            "android:tint applies a tint to the ImageView image.",
            "Module 2, android:tint",
        ),
    ]


def module3():
    return [
        single(
            "What is an Android Layout?",
            ("The user interface that holds the UI controls shown on an Activity screen",
             "The module says a Layout defines the UI that holds the controls or widgets on an Activity screen."),
            [
                ("The series of Activity states from creation to destruction",
                 "That series is the Activity lifecycle, not a layout."),
                ("A Kotlin variable that cannot be reassigned",
                 "A read-only Kotlin binding is val. A layout is the UI structure."),
                ("The Android Studio status bar",
                 "The status bar shows IDE messages. A layout holds the screen's controls."),
            ],
            "A layout defines the user interface that holds the widgets on an Activity screen.",
            "Module 3, What is a Layout?",
        ),
        single(
            "How does the module describe a typical application interface?",
            ("A combination of Views and ViewGroups",
             "The module says an application interface is generally a combination of Views and ViewGroups."),
            [
                ("Only one ImageView and no containers",
                 "The module describes a combination of Views and ViewGroups, not a single image."),
                ("Only Kotlin functions, with no widgets",
                 "Kotlin supplies behavior. The interface itself is Views and ViewGroups."),
                ("A list of Android version code names",
                 "Code names are the version timeline. The interface is Views and ViewGroups."),
            ],
            "An application interface is generally Views and ViewGroups together.",
            "Module 3, Views and ViewGroups",
        ),
        single(
            "What is a View?",
            ("A UI component that draws itself and handles events. Examples include TextView, ImageView, EditText, and RadioButton",
             "That is the module's definition, including those widget examples. Views are generally called widgets."),
            [
                ("A parent container that defines layout properties for children",
                 "A parent container is a ViewGroup."),
                ("The vertical scroller that allows only one direct child",
                 "That specific container is a ScrollView, which is a ViewGroup."),
                ("The Intent extra that carries a username",
                 "An Intent extra carries data between Activities. A View is a widget."),
            ],
            "A View is a widget: it draws itself and handles events. TextView, ImageView, EditText, and RadioButton are examples.",
            "Module 3, View",
        ),
        single(
            "What is a ViewGroup?",
            ("A base class for layouts. It holds other Views or ViewGroups and acts as their parent",
             "The module calls ViewGroup the base class for layouts and a parent container for child Views."),
            [
                ("A widget such as a RadioButton",
                 "RadioButton is given as a View example. A ViewGroup is the container."),
                ("A read-only Kotlin value",
                 "A read-only value is val."),
                ("The onResume callback",
                 "onResume is a lifecycle callback, not a container."),
            ],
            "A ViewGroup is the layout base class: a parent that holds Views or other ViewGroups.",
            "Module 3, ViewGroup",
        ),
        match(
            "Match each layout with the idea the module stresses.",
            [
                ("Positions widgets with constraints and can avoid deep nesting", "constraint"),
                ("Arranges children in a row or column using orientation", "linear"),
                ("Places children in rows and columns and draws no cell borders", "table"),
                ("A placeholder that can stack views, often with one child", "frame"),
                ("A two-dimensional scrollable grid filled through an adapter", "grid"),
                ("A card with rounded corners and elevation", "card"),
                ("Vertical scrolling with one direct child", "scroll"),
                ("Horizontal scrolling whose child can be a layout", "hscroll"),
            ],
            [
                ("constraint", "ConstraintLayout"),
                ("linear", "LinearLayout"),
                ("table", "TableLayout"),
                ("frame", "FrameLayout"),
                ("grid", "GridView"),
                ("card", "CardView"),
                ("scroll", "ScrollView"),
                ("hscroll", "HorizontalScrollView"),
            ],
            "ConstraintLayout uses constraints, LinearLayout uses orientation, and the other containers match the Module 3 table.",
            "Module 3, layout types",
            "Name the layout.",
        ),
        single(
            "What does the module say ConstraintLayout helps you avoid?",
            ("Deeply nested layouts, which it presents as better for UI performance",
             "The ConstraintLayout row says it can help avoid deeply nested layouts and is presented as improving UI performance."),
            [
                ("All use of android:id",
                 "Ids are how code finds views. ConstraintLayout is about positioning with constraints."),
                ("The Activity lifecycle",
                 "The lifecycle is a separate module. ConstraintLayout is a positioning layout."),
                ("Horizontal orientation in a LinearLayout",
                 "Orientation belongs to LinearLayout. ConstraintLayout's point is flexible constraints and less nesting."),
            ],
            "ConstraintLayout positions widgets with constraints, supports drag-and-drop, and is presented as a way to avoid deep nesting and improve performance.",
            "Module 3, ConstraintLayout",
        ),
        single(
            "How does LinearLayout arrange its children?",
            ("Sequentially, in a horizontal row or a vertical column, using android:orientation",
             "That is the LinearLayout row: sequential arrangement controlled by android:orientation."),
            [
                ("In a two-dimensional grid fed by an adapter",
                 "A two-dimensional adapter grid is GridView."),
                ("Stacked on top of each other in a placeholder",
                 "Stacking views in a placeholder is FrameLayout."),
                ("Only by wallpaper-colored Material You themes",
                 "Material You is an Android 12 feature, not how LinearLayout places children."),
            ],
            "LinearLayout arranges children in a horizontal row or a vertical column based on android:orientation.",
            "Module 3, LinearLayout",
        ),
        single(
            "What is true of TableLayout in this module?",
            ("It places child Views in rows and columns and does not display border lines. A TableRow is like an HTML table row",
             "The table row says there are no border lines, and that TableRow is analogous to an HTML table row."),
            [
                ("It always draws grid lines around every cell",
                 "The module says TableLayout does not display border lines for rows, columns, or cells."),
                ("It is the vertical scroller with one direct child",
                 "That is ScrollView."),
                ("It is Kotlin's replacement for switch",
                 "Kotlin's multi-branch form is when. TableLayout is a row-and-column container."),
            ],
            "TableLayout uses rows and columns without drawing borders. TableRow corresponds to an HTML table row.",
            "Module 3, TableLayout",
        ),
        single(
            "How does the module present FrameLayout?",
            ("As a placeholder that can put Views on top of one another, commonly holding a single child",
             "The FrameLayout row says it is an area for Views, supports stacking, and is commonly used for a single child."),
            [
                ("As a card with rounded corners and a shadow",
                 "Rounded corners and elevation describe CardView."),
                ("As horizontal-only scrolling",
                 "Horizontal scrolling is HorizontalScrollView."),
                ("As the constraint system that avoids nested layouts",
                 "That is ConstraintLayout."),
            ],
            "FrameLayout is a placeholder that can stack Views, and it is commonly used to hold a single child.",
            "Module 3, FrameLayout",
        ),
        single(
            "How does GridView get its items?",
            ("Through an adapter that can take data from an array or a database and turn items into Views",
             "The GridView row says items can be populated by an adapter from sources such as an array or database."),
            [
                ("By setting android:hint on each cell",
                 "android:hint is an empty EditText placeholder, not how a GridView is filled."),
                ("By calling onDestroy for each row",
                 "onDestroy cleans up an Activity. GridView uses an adapter."),
                ("By a TableRow that draws HTML borders",
                 "TableLayout uses TableRow and does not draw borders. GridView uses an adapter."),
            ],
            "GridView shows a two-dimensional scrollable grid. An adapter pulls from a source such as an array or database and converts items into Views.",
            "Module 3, GridView",
        ),
        single(
            "What is an Adapter, in the quick review?",
            ("A bridge between a data source and a collection UI. It converts data items into Views",
             "The quick review defines an Adapter as that bridge."),
            [
                ("The drawable used as a Button background",
                 "The Button background drawable is android:background."),
                ("The read-only Kotlin keyword",
                 "The read-only keyword is val."),
                ("The bar that shows IDE warnings",
                 "IDE warnings show on the status bar."),
            ],
            "An Adapter bridges a data source and a collection UI by turning data items into Views.",
            "Quick review, Adapter",
        ),
        single(
            "What does CardView add to the content it holds?",
            ("A card-like container with rounded corners and elevation or shadow",
             "The CardView row describes rounded corners and elevation/shadow for a richer UI."),
            [
                ("Mandatory cell borders like a spreadsheet",
                 "TableLayout is the row-and-column container, and it does not draw borders."),
                ("Horizontal scrolling of one child",
                 "Horizontal scrolling is HorizontalScrollView."),
                ("A password input type",
                 "Password is an android:inputType example, not CardView."),
            ],
            "CardView shows content in a card with rounded corners and elevation.",
            "Module 3, CardView",
        ),
        single(
            "How many direct children does a ScrollView have?",
            ("One. To hold many Views, put a ViewGroup such as a LinearLayout in that single child slot",
             "The module says ScrollView has one direct child, and that a ViewGroup such as LinearLayout should be that child when you need many Views."),
            [
                ("As many as android:maxLines allows",
                 "android:maxLines limits text lines. ScrollView's limit is one direct child."),
                ("Two, which must be stacked with FrameLayout rules",
                 "FrameLayout can stack views. ScrollView allows one direct child."),
                ("None. ScrollView draws its own rows",
                 "ScrollView scrolls a child. It does not invent rows of its own."),
            ],
            "ScrollView scrolls vertically and has one direct child. Use a ViewGroup such as LinearLayout when you need many Views inside it.",
            "Module 3, ScrollView",
        ),
        single(
            "What does HorizontalScrollView provide?",
            ("Horizontal scrolling. Its child can itself be a layout such as LinearLayout",
             "That is the HorizontalScrollView row."),
            [
                ("Vertical scrolling of one direct child",
                 "Vertical scrolling is ScrollView."),
                ("A two-dimensional grid",
                 "A two-dimensional grid is GridView."),
                ("Dynamic colors taken from the wallpaper",
                 "Wallpaper-based theming is Material You on Android 12."),
            ],
            "HorizontalScrollView scrolls horizontally, and its child can be a layout manager such as LinearLayout.",
            "Module 3, HorizontalScrollView",
        ),
        single(
            "What does wrap_content mean?",
            ("Use only as much space as the content requires",
             "The frequently tested table defines wrap_content that way."),
            [
                ("Expand to the available size of the parent",
                 "Expanding to the parent is match_parent."),
                ("Hide the view but keep its space",
                 "Hidden while still taking space is INVISIBLE."),
                ("Size the text in scale-independent pixels",
                 "Scale-independent pixels are sp. wrap_content is a width or height value."),
            ],
            "wrap_content uses only as much space as the content requires.",
            "Module 3, wrap_content",
        ),
        single(
            "What does match_parent mean?",
            ("Expand to the available size of the parent",
             "The frequently tested table defines match_parent that way."),
            [
                ("Use only as much space as the content requires",
                 "Shrinking to the content is wrap_content."),
                ("Hide the view and take no space",
                 "Hidden with no space is GONE."),
                ("Align the view's content to the center",
                 "Content alignment is gravity, not match_parent."),
            ],
            "match_parent expands to the available size of the parent.",
            "Module 3, match_parent",
        ),
        single(
            "Which attribute aligns content inside a View, such as text in a TextView or Button?",
            ("gravity",
             "The module says gravity aligns a View's content, such as text inside a TextView or Button."),
            [
                ("layout_gravity",
                 "layout_gravity positions the View inside its parent. gravity aligns what is inside the View."),
                ("orientation",
                 "orientation sets a LinearLayout's row or column direction."),
                ("margin",
                 "margin is space outside the View boundary."),
            ],
            "gravity aligns content inside a View. layout_gravity positions the View inside its parent.",
            "Module 3, gravity",
        ),
        single(
            "What does layout_gravity control?",
            ("The position of a View within its parent, in layouts that support it",
             "That is the layout-attribute definition of layout_gravity."),
            [
                ("Alignment of text inside the View",
                 "Alignment inside the View is gravity."),
                ("Space outside the View",
                 "Space outside the View is margin."),
                ("The unique id used from Kotlin",
                 "The id is android:id."),
            ],
            "layout_gravity positions the View inside its parent. gravity aligns the content inside the View.",
            "Module 3, layout_gravity",
        ),
        single(
            "Where is padding applied?",
            ("Inside the View boundary, between the content and the edge",
             "The module says padding is space inside the boundary."),
            [
                ("Outside the View, separating it from other Views",
                 "Space outside the boundary is margin."),
                ("Only on the text size, in sp",
                 "sp is the unit recommended for text size. Padding is inner space."),
                ("On the Activity, as the onPause callback",
                 "onPause is a lifecycle callback. Padding is inner space in the View."),
            ],
            "Padding is space inside the View boundary. Margin is space outside it.",
            "Module 3, padding",
        ),
        single(
            "Where is margin applied?",
            ("Outside the View boundary, separating it from other Views or the parent",
             "The module says margin is space outside the boundary."),
            [
                ("Inside the boundary, between the content and the edge",
                 "Space inside the boundary is padding."),
                ("On the font scale only",
                 "Font scale is why text size uses sp. Margin is outer space."),
                ("As the image source of an ImageView",
                 "The image source is android:src."),
            ],
            "Margin is space outside the View boundary. Padding is space inside it.",
            "Module 3, margin",
        ),
        single(
            "What is dp used for?",
            ("Density-independent pixels, for View dimensions, margins, and padding",
             "The frequently tested table assigns dp to dimensions, margins, and padding."),
            [
                ("Text size that follows the user's font-size preference",
                 "Text size that respects font-size preferences uses sp."),
                ("A visibility value that keeps empty space",
                 "The visibility value that keeps space is INVISIBLE."),
                ("The Kotlin assignment operator",
                 "Assignment is =. dp is a dimension unit."),
            ],
            "dp means density-independent pixels, used for dimensions, margins, and padding.",
            "Module 3, dp",
        ),
        single(
            "What is sp used for?",
            ("Scale-independent pixels, recommended for text size, and they respect font-size preferences",
             "The table says sp is for text size and respects font-size preferences."),
            [
                ("Width, height, margin, and padding",
                 "Those dimensions use dp."),
                ("Hiding a view without leaving a gap",
                 "Hiding a view without leaving space is GONE."),
                ("Comparing two Kotlin values for equality",
                 "Equality comparison is ==. sp is the text-size unit."),
            ],
            "sp means scale-independent pixels. Use it for text size so font-size preferences are respected.",
            "Module 3, sp",
        ),
        single(
            "What does INVISIBLE mean?",
            ("The View is hidden but still occupies layout space",
             "The frequently tested table says INVISIBLE hides the View and still occupies space."),
            [
                ("The View is hidden and occupies no layout space",
                 "Hidden with no space is GONE."),
                ("The View expands to the parent",
                 "Expanding to the parent is match_parent."),
                ("The View is in the onResume state",
                 "onResume means the Activity is ready for interaction. INVISIBLE is a visibility value."),
            ],
            "INVISIBLE hides the View but leaves its layout space occupied.",
            "Module 3, INVISIBLE",
        ),
        single(
            "What does GONE mean?",
            ("The View is hidden and does not occupy layout space",
             "The table says GONE hides the View and does not occupy space."),
            [
                ("The View is hidden but still occupies layout space",
                 "Hidden while still taking space is INVISIBLE."),
                ("The View uses only the space of its content",
                 "Sizing to the content is wrap_content."),
                ("The Activity is being destroyed",
                 "Destruction is onDestroy. GONE is a visibility value."),
            ],
            "GONE hides the View and does not keep its layout space.",
            "Module 3, GONE",
        ),
        single(
            "What is android:id used for on a layout View?",
            ("A unique identifier so Kotlin or Java code can reference the View",
             "The layout-attribute table says id / android:id is the unique identifier used from Kotlin or Java."),
            [
                ("The direction of children in a LinearLayout",
                 "Child direction is orientation."),
                ("Space outside the View",
                 "Outer space is margin."),
                ("The image tint",
                 "Image tint is android:tint."),
            ],
            "android:id uniquely identifies a View so code can reference it.",
            "Module 3, android:id",
        ),
    ]


def module4():
    return [
        single(
            "What is the Android lifecycle?",
            ("The series of states an Activity or Fragment goes through from creation to destruction",
             "The module defines the lifecycle as that series of states."),
            [
                ("The list of dessert code names from Cupcake to Vanilla Ice Cream",
                 "Code names are the version timeline. The lifecycle is the Activity or Fragment state series."),
                ("The XML file that holds Buttons and EditTexts",
                 "XML defines the visual interface. The lifecycle is the state series."),
                ("The Kotlin when expression",
                 "when is a conditional. The lifecycle is creation through destruction."),
            ],
            "The lifecycle is the series of states an Activity or Fragment goes through from creation to destruction.",
            "Module 4, definition",
        ),
        single(
            "How does Android interact with an app's Activity?",
            ("By calling functions in the Activity class, even when the programmer does not visibly call them",
             "The module says Android calls those functions at the right time, even if the programmer does not visibly call them."),
            [
                ("Only when the programmer calls onCreate, onStart, and onResume in order from main",
                 "The module says these are not ordinary functions you call yourself in a normal sequence. Android calls them."),
                ("By rewriting the XML layout on every frame",
                 "XML defines the interface. Android drives the Activity by calling lifecycle functions."),
                ("By sending the app a Google Play download",
                 "Google Play distributes apps. Lifecycle interaction is Android calling Activity functions."),
            ],
            "Android calls lifecycle functions on the Activity even when your own code does not visibly call them.",
            "Module 4, interaction",
        ),
        single(
            "What does overriding onCreate do?",
            ("It supplies the version of that function Android should run when the create event occurs",
             "The module says an override supplies the version Android executes for that lifecycle event."),
            [
                ("It stops Android from ever calling onCreate",
                 "Overriding does not block the call. It supplies the body Android runs."),
                ("It replaces the XML layout with a Kotlin when expression",
                 "when is a conditional. An onCreate override is the create callback Android runs."),
                ("It marks the Activity INVISIBLE",
                 "INVISIBLE is a view visibility value, not what an override means."),
            ],
            "Overriding onCreate gives Android the function body to run when the Activity is created.",
            "Module 4, override",
        ),
        single(
            "Why does the module say lifecycle knowledge matters?",
            ("So you know when to save data, pause work, release resources, and restore information if something such as a phone call interrupts the user",
             "The module's example is a user typing a reminder when a phone call interrupts the app."),
            [
                ("So you can skip onCreate and start the app in onDestroy",
                 "onDestroy is the end of the lifecycle, not a shortcut around onCreate."),
                ("So the Layout Editor can assign dessert code names",
                 "Code names are version history. Lifecycle knowledge is about interruptions and state changes."),
                ("So wrap_content can expand to the parent",
                 "wrap_content and match_parent are layout sizes, not the reason the lifecycle is taught."),
            ],
            "The phone-call example is about saving data, pausing work, releasing resources, and restoring information when the app is interrupted.",
            "Module 4, why it matters",
        ),
        match(
            "Match each simplified lifecycle phase with its callback.",
            [
                ("Being created: initialize the Activity and prepare the UI", "create"),
                ("Starting: becoming visible, not yet interactive", "start"),
                ("Resuming: ready for interaction, including after a pause", "resume"),
                ("Pausing: losing foreground focus", "pause"),
                ("Stopping: no longer visible", "stop"),
                ("Being destroyed: final cleanup", "destroy"),
            ],
            [
                ("create", "onCreate"),
                ("start", "onStart"),
                ("resume", "onResume"),
                ("pause", "onPause"),
                ("stop", "onStop"),
                ("destroy", "onDestroy"),
            ],
            "The running phase sits between onResume and onPause. The callbacks follow the phase table.",
            "Module 4, phases",
            "Name the callback.",
        ),
        single(
            "What is onCreate commonly used for?",
            ("Initialization, UI setup, setContentView(), and preparing graphics or sound",
             "The callback table lists those as the common work when the Activity is created."),
            [
                ("Releasing resources because the Activity is no longer visible",
                 "Releasing resources when the Activity is no longer visible is onStop."),
                ("The final dismantling of the Activity",
                 "Final dismantling is onDestroy."),
                ("Only reloading data after the user returns from a pause",
                 "The module's reload example belongs to onResume."),
            ],
            "onCreate is where the Activity is initialized, the UI is set up with setContentView(), and graphics or sound can be prepared.",
            "Module 4, onCreate",
        ),
        single(
            "What is true of onStart?",
            ("The Activity is becoming visible to the user but is not yet interactive",
             "The module describes onStart as the starting phase: visible, not yet interactive."),
            [
                ("The Activity is in the foreground and ready for interaction",
                 "Ready for interaction is onResume, the running side of the lifecycle."),
                ("The Activity is no longer visible",
                 "No longer visible is onStop."),
                ("The Activity is being destroyed",
                 "Destruction is onDestroy."),
            ],
            "onStart runs as the Activity becomes visible, before it is interactive.",
            "Module 4, onStart",
        ),
        single(
            "What does the module say about onResume?",
            ("The Activity is becoming active. It can also be reached after a pause, and it is an example place to reload saved user data",
             "The phase table says onResume can be reached after a paused state, and the callback notes use reloading saved user data as the example."),
            [
                ("It runs only once, before onCreate",
                 "The flow is onCreate, then onStart, then onResume. onResume can also run again after a pause."),
                ("It means the Activity is no longer visible",
                 "No longer visible is onStop."),
                ("It is the final cleanup callback",
                 "Final cleanup is onDestroy."),
            ],
            "onResume makes the Activity active and can run again after a pause. The module's example is reloading saved user data.",
            "Module 4, onResume",
        ),
        single(
            "What belongs in onPause?",
            ("Pause tasks that need not continue, stop animations, save unsaved data, and release resources that do not need to stay active",
             "The callback table assigns those jobs to onPause, when the Activity is losing foreground focus."),
            [
                ("Call setContentView() for the first time",
                 "setContentView() is named under onCreate."),
                ("Write the final destruction cleanup",
                 "Final cleanup is onDestroy."),
                ("Inflate the layout before the Activity exists",
                 "The Activity is already past creation by the time it pauses."),
            ],
            "onPause is the place to pause work, stop animations, save unsaved data, and release resources that do not need to keep running.",
            "Module 4, onPause",
        ),
        single(
            "When does onStop run, and what can it do?",
            ("When the Activity is no longer visible. It can release resources or write information to persistent storage",
             "That is the onStop row: no longer visible, release or persist."),
            [
                ("When the Activity is visible but not yet interactive",
                 "Visible but not interactive is onStart."),
                ("When the Activity is first created",
                 "Creation is onCreate."),
                ("Only when a Button's android:hint is empty",
                 "android:hint is an EditText placeholder. onStop is the not-visible callback."),
            ],
            "onStop runs when the Activity is no longer visible. Use it to release resources or persist information.",
            "Module 4, onStop",
        ),
        single(
            "What is onDestroy?",
            ("The final opportunity to dismantle the Activity in an orderly way before it is removed",
             "The module describes onDestroy as that final cleanup."),
            [
                ("The callback that makes the Activity interactive",
                 "Becoming interactive is onResume."),
                ("The callback that only saves a pause-time draft",
                 "Saving unsaved data as focus is lost is onPause. onDestroy is final dismantling."),
                ("The Layout Editor's preview mode",
                 "The Layout Editor edits the UI. onDestroy is the last lifecycle callback."),
            ],
            "onDestroy is the final chance to dismantle the Activity in an orderly way.",
            "Module 4, onDestroy",
        ),
        single(
            "Which flow matches the module?",
            ("onCreate → onStart → onResume → Running → onPause → onStop → onDestroy",
             "That is the flow the module says to memorize."),
            [
                ("onCreate → onResume → onStart → Running → onStop → onPause → onDestroy",
                 "onStart comes before onResume, and onPause comes before onStop."),
                ("onStart → onCreate → onPause → onResume → onDestroy → onStop",
                 "Creation is first, and destruction is last. Pause comes before stop."),
                ("onResume → onCreate → onStart → onDestroy → onPause → onStop",
                 "The module starts at onCreate and ends at onDestroy."),
            ],
            "Memorize onCreate, onStart, onResume, Running, onPause, onStop, onDestroy.",
            "Module 4, flow",
        ),
        single(
            "Who calls the lifecycle methods during normal state changes?",
            ("Android, in response to Activity state changes. They are not ordinary functions you call yourself in sequence",
             "The module's important idea is that Android calls them. You do not drive that sequence by hand."),
            [
                ("The Layout Editor, once per XML attribute",
                 "The Layout Editor edits the interface. Android calls lifecycle methods."),
                ("findViewById(), after every click",
                 "findViewById retrieves a View. It does not walk the lifecycle."),
                ("The programmer, from a while loop in the order shown",
                 "The module says not to treat them as ordinary functions you call in a normal sequence."),
            ],
            "Android calls lifecycle methods when the Activity state changes. You do not call that sequence yourself.",
            "Module 4, who calls them",
        ),
    ]


def module5():
    return [
        single(
            "What is a variable in this module?",
            ("A value stored in memory that can be referred to by a name",
             "That is the module's definition of a variable."),
            [
                ("A ViewGroup that holds child widgets",
                 "A container for widgets is a ViewGroup."),
                ("An XML attribute that sets text size",
                 "Text size is android:textSize. A variable is a named value in memory."),
                ("The onStart lifecycle callback",
                 "onStart is an Activity callback, not a named value in memory."),
            ],
            "A variable is a named value stored in memory.",
            "Module 5, variables",
        ),
        single(
            "What limit does the module put on variable names?",
            ("The programmer may choose them as long as they do not break Kotlin naming rules or use restricted keywords",
             "The module allows chosen names that respect naming rules and reserved keywords."),
            [
                ("They must be Android dessert code names",
                 "Dessert names are the version table. Variable names follow Kotlin rules."),
                ("They must be android:id values from the XML file",
                 "android:id identifies a View. A Kotlin variable name follows naming rules."),
                ("They can only be val or var, with no other characters",
                 "val and var are the keywords that declare variables. The name itself is chosen by the programmer."),
            ],
            "You choose the name, provided it follows Kotlin naming rules and avoids restricted keywords.",
            "Module 5, naming",
        ),
        single(
            "Why does the module recommend a consistent naming convention?",
            ("So names stay understandable and consistent throughout the program",
             "That is the reason given for a consistent convention."),
            [
                ("So Android will call onCreate",
                 "Android calls onCreate because of the lifecycle, not because of variable names."),
                ("So match_parent can see the variable",
                 "match_parent is a layout size. Naming is about readable code."),
                ("So the name can be used as a Google Play package",
                 "The package name is project configuration. A naming convention keeps variables understandable."),
            ],
            "A consistent convention keeps variable names understandable through the program.",
            "Module 5, naming convention",
        ),
        match(
            "Match each Kotlin type with what it stores.",
            [
                ("Integers and whole numbers", "int"),
                ("Larger whole-number values", "long"),
                ("Floating-point numbers with decimal precision", "float"),
                ("Floating-point numbers when greater precision than Float is needed", "double"),
                ("Only true or false", "bool"),
                ("A single alphanumeric character", "char"),
                ("Text and keyboard characters", "string"),
            ],
            [
                ("int", "Int"),
                ("long", "Long"),
                ("float", "Float"),
                ("double", "Double"),
                ("bool", "Boolean"),
                ("char", "Char"),
                ("string", "String"),
            ],
            "Int and Long are whole numbers, Float and Double are decimal, Boolean is true or false, Char is one character, and String is text.",
            "Module 5, data types",
            "Name the type.",
        ),
        single(
            "What does val mean?",
            ("A read-only value that cannot be changed during execution. Use it when the value does not need to change",
             "The val row says it cannot be changed during execution and is for values that do not need to change."),
            [
                ("A mutable variable that can be updated",
                 "A value that can be updated is var."),
                ("A layout width that wraps the content",
                 "Wrapping the content is wrap_content."),
                ("A lifecycle callback",
                 "val is a Kotlin declaration keyword, not a lifecycle callback."),
            ],
            "val is read-only after initialization. Use it when the value does not need to change.",
            "Module 5, val",
        ),
        single(
            "What does var mean?",
            ("A mutable variable whose value can be changed during execution",
             "The var row says the value can be changed, and to use it when the value needs to be updated."),
            [
                ("A value that cannot be reassigned after initialization",
                 "A value that cannot be reassigned is val."),
                ("An XML id",
                 "An XML id is android:id. var declares a mutable Kotlin variable."),
                ("The logical NOT operator",
                 "Logical NOT is !."),
            ],
            "var can be changed during execution. Use it when the value needs to be updated.",
            "Module 5, var",
        ),
        match(
            "Classify each declaration from the module.",
            [
                ("val battleOfHastings = 1066", "val"),
                ("val pi = 3.14f", "val"),
                ("val beerIsTasty = true", "val"),
                ("val appName = \"Express Yourself\"", "val"),
                ("var worldRecord100m = 9.63f", "var"),
                ("var millisecondsSince1970 = 1544693462311", "var"),
                ("var isItRaining = false", "var"),
                ("var contactName = \"Geralt\"", "var"),
            ],
            [
                ("val", "val, read-only"),
                ("var", "var, mutable"),
            ],
            "battleOfHastings, pi, beerIsTasty, and appName are val. The record, the millisecond count, the rain flag, and contactName are var.",
            "Module 5, examples",
            "Choose val or var.",
        ),
        single(
            "Which module example is a read-only decimal value?",
            ("val pi = 3.14f",
             "The module lists val pi = 3.14f among the read-only examples, and the value is a decimal."),
            [
                ("var worldRecord100m = 9.63f",
                 "9.63f is a decimal, but this example is var, so it can change."),
                ("var isItRaining = false",
                 "false is a Boolean, and this example is var."),
                ("val appName = \"Express Yourself\"",
                 "appName is val, but the value is text, not a decimal."),
            ],
            "val pi = 3.14f is the read-only decimal in the module's examples.",
            "Module 5, pi example",
        ),
        match(
            "Match each operator with its behavior in the module.",
            [
                ("Assigns a value", "assign"),
                ("Adds numbers, or concatenates strings", "plus"),
                ("Subtracts", "minus"),
                ("Divides", "div"),
                ("Multiplies", "mul"),
                ("Increases a numeric value", "inc"),
                ("Decreases a numeric value", "dec"),
            ],
            [
                ("assign", "="),
                ("plus", "+"),
                ("minus", "-"),
                ("div", "/"),
                ("mul", "*"),
                ("inc", "++"),
                ("dec", "--"),
            ],
            "= assigns, + adds or concatenates, and ++ and -- increment and decrement.",
            "Module 5, arithmetic operators",
            "Pick the operator.",
        ),
        single(
            "What does + do with strings in this module?",
            ("Concatenation",
             "The operator table says + is addition for numbers and concatenation for strings."),
            [
                ("Equality comparison",
                 "Equality comparison is ==."),
                ("Logical AND",
                 "Logical AND is &&."),
                ("Assignment",
                 "Assignment is =."),
            ],
            "With strings, + concatenates. With numbers, it adds.",
            "Module 5, string +",
        ),
        match(
            "Match each comparison or logical operator with its meaning.",
            [
                ("Equality comparison, with a true or false result", "eq"),
                ("Not equal", "neq"),
                ("Greater than", "gt"),
                ("Less than", "lt"),
                ("Greater than or equal to", "gte"),
                ("Less than or equal to", "lte"),
                ("Logical NOT, the opposite Boolean", "not"),
                ("Logical AND", "and"),
                ("Logical OR", "or"),
            ],
            [
                ("eq", "=="),
                ("neq", "!="),
                ("gt", ">"),
                ("lt", "<"),
                ("gte", ">="),
                ("lte", "<="),
                ("not", "!"),
                ("and", "&&"),
                ("or", "||"),
            ],
            "== compares, ! is NOT, && is AND, and || is OR.",
            "Module 5, comparison and logic",
            "Pick the operator.",
        ),
        single(
            "What does if do?",
            ("Evaluates a condition and runs code based on whether that condition is true or false",
             "That is the module's description of if."),
            [
                ("Checks one value against many branches and replaces switch",
                 "Checking many possible values, as a replacement for switch, is when."),
                ("Declares a mutable variable",
                 "A mutable declaration is var."),
                ("Starts another Activity",
                 "Starting another Activity is startActivity with an Intent."),
            ],
            "if evaluates a condition and runs code according to true or false.",
            "Module 5, if",
        ),
        single(
            "What does if / else add?",
            ("One path when the condition is true and another path when it is false",
             "The module says if / else provides those two paths."),
            [
                ("A match against many values, in place of switch",
                 "Many branches in place of switch is when."),
                ("A read-only declaration",
                 "A read-only declaration is val."),
                ("A layout constraint",
                 "Constraints belong to ConstraintLayout, not if / else."),
            ],
            "if / else gives one path for true and another path for false.",
            "Module 5, if / else",
        ),
        single(
            "What is when?",
            ("A check of one value against multiple possible values. The module presents it as Kotlin's replacement for switch",
             "That is the when row: multiple values, and the replacement for switch in other languages."),
            [
                ("A two-path branch with only true and false",
                 "A true path and a false path are if / else. when handles multiple possible values."),
                ("The assignment operator",
                 "Assignment is =."),
                ("The callback Android runs when an Activity is created",
                 "The create callback is onCreate. when is a Kotlin conditional."),
            ],
            "when checks a value against multiple possibilities and is Kotlin's replacement for switch.",
            "Module 5, when",
        ),
    ]


def module_ui():
    return [
        single(
            "What does the XML layout define?",
            ("The visual interface: Views, attributes, dimensions, text, positioning, and other UI properties",
             "The consolidated table assigns the visual interface to the XML layout."),
            [
                ("Click behavior, calculations, and navigation",
                 "Behavior, events, calculations, and navigation are the Kotlin side."),
                ("The Activity lifecycle order",
                 "The lifecycle is Android calling Activity callbacks. XML describes the interface."),
                ("The dessert code name of the phone",
                 "Code names are the version table. XML describes Views and attributes."),
            ],
            "XML defines the visual interface: Views, attributes, dimensions, text, and positioning.",
            "UI concepts, XML",
        ),
        single(
            "What does Kotlin do in the XML-and-Kotlin split?",
            ("Implements behavior and logic, handles events, reads input, calculates, and controls navigation",
             "That is the Kotlin row in the consolidated table."),
            [
                ("Declares the visual tree, dimensions, and positioning",
                 "The visual tree and positioning belong to the XML layout."),
                ("Stores the app on Google Play",
                 "Google Play is the distribution ecosystem. Kotlin is the behavior in the app."),
                ("Replaces android:id so views cannot be found",
                 "android:id exists so Kotlin can reference a View. Kotlin does not replace that id."),
            ],
            "Kotlin implements behavior: events, input, calculations, and navigation.",
            "UI concepts, Kotlin",
        ),
        single(
            "What does setContentView() do?",
            ("Connects an Activity to an XML layout",
             "The table says setContentView() connects an Activity to an XML layout."),
            [
                ("Reads an EditText as a String",
                 "Reading the field is editText.text.toString()."),
                ("Sends a key-value pair to another Activity",
                 "Sending data on an Intent is putExtra."),
                ("Ends the current Activity so Back cannot return",
                 "Ending the current Activity is finish()."),
            ],
            "setContentView() connects the Activity to an XML layout.",
            "UI concepts, setContentView",
        ),
        single(
            "What does setContentView(R.layout.activity_main) connect?",
            ("The Activity to the XML layout named activity_main",
             "The code table says that call connects the Activity to the layout named activity_main."),
            [
                ("The Activity to activity_profile",
                 "activity_profile is the other layout in the Login → Profile sample. This call names activity_main."),
                ("A Button click to a Toast",
                 "A click is setOnClickListener. This call attaches the layout."),
                ("An ImageView to centerCrop",
                 "centerCrop is a scaleType. This call attaches activity_main."),
            ],
            "setContentView(R.layout.activity_main) connects the Activity to the layout named activity_main.",
            "UI concepts, activity_main",
        ),
        single(
            "What does findViewById() do?",
            ("Retrieves a View from the XML layout so Kotlin can work with it",
             "The table says findViewById() retrieves a View from the XML layout."),
            [
                ("Creates the XML file",
                 "The XML file defines the interface. findViewById retrieves a View that is already in it."),
                ("Declares a read-only Kotlin value with no View involved",
                 "val declares a read-only value. findViewById is how code obtains a View."),
                ("Destroys the Activity",
                 "Destruction is onDestroy, or finish() for the current Activity. findViewById looks up a View."),
            ],
            "findViewById() retrieves a View from the XML layout so Kotlin can use it.",
            "UI concepts, findViewById",
        ),
        single(
            "What does findViewById<Button>(R.id.btnLogin) return?",
            ("The Button whose XML id is btnLogin",
             "The code table says it finds the Button whose XML ID is btnLogin."),
            [
                ("The EditText named etUsername",
                 "etUsername is a different id. This call looks up R.id.btnLogin."),
                ("The profile TextView",
                 "The profile text id in the sample is tvUsername."),
                ("Every View in the layout",
                 "The call looks up one id, btnLogin, as a Button."),
            ],
            "findViewById<Button>(R.id.btnLogin) finds the Button whose XML id is btnLogin.",
            "UI concepts, btnLogin",
        ),
        single(
            "What does android:id=\"@+id/btnLogin\" do?",
            ("Assigns an id to an XML View so Kotlin can find and use it",
             "The code table says that attribute assigns an id so Kotlin can find the View."),
            [
                ("Starts ProfileActivity",
                 "Starting the next Activity is startActivity with an Intent."),
                ("Reads the typed username",
                 "Reading the field is text.toString()."),
                ("Sets the Button's click block",
                 "The click block is setOnClickListener."),
            ],
            "android:id=\"@+id/btnLogin\" assigns the id Kotlin later looks up.",
            "UI concepts, @+id",
        ),
        single(
            "What does editText.text.toString() do?",
            ("Reads the user's EditText input as a String",
             "The code table says it reads the EditText input as a String."),
            [
                ("Shows a temporary Toast",
                 "A temporary message is Toast.makeText(...).show()."),
                ("Connects the Activity to a layout",
                 "Connecting the layout is setContentView()."),
                ("Compares two values for equality",
                 "Equality comparison is ==. toString() here reads the field."),
            ],
            "editText.text.toString() reads the EditText as a String.",
            "UI concepts, toString",
        ),
        single(
            "What does button.setOnClickListener { ... } do?",
            ("Runs the enclosed code when the Button is clicked",
             "The code table says the listener runs the enclosed code when the Button is clicked."),
            [
                ("Runs the block once when the Activity is created, with no click",
                 "Work at creation belongs in onCreate. This listener waits for the click."),
                ("Declares a when branch",
                 "when is a conditional. This is a click listener."),
                ("Sets android:hint",
                 "android:hint is XML placeholder text. The listener runs Kotlin when the Button is clicked."),
            ],
            "setOnClickListener runs the enclosed code when the Button is clicked.",
            "UI concepts, click listener",
        ),
        single(
            "What does Toast.makeText(...).show() do?",
            ("Creates and displays a temporary message",
             "The code table says it creates and displays a temporary message."),
            [
                ("Opens another Activity and passes a username",
                 "Opening another Activity and passing data is an Intent with putExtra and startActivity."),
                ("Saves the Activity in onPause",
                 "onPause is where you pause and save. A Toast is a temporary message."),
                ("Sets the layout width to match_parent",
                 "match_parent is a layout size. A Toast is a temporary message."),
            ],
            "Toast.makeText(...).show() creates and displays a temporary message.",
            "UI concepts, Toast",
        ),
        single(
            "How do Toast.LENGTH_SHORT and Toast.LENGTH_LONG differ?",
            ("LENGTH_SHORT is the short duration and LENGTH_LONG is the longer duration",
             "The code table assigns the short duration to LENGTH_SHORT and the longer duration to LENGTH_LONG."),
            [
                ("LENGTH_SHORT hides the View and LENGTH_LONG keeps its space",
                 "Hiding with or without space is GONE versus INVISIBLE. These constants are Toast durations."),
                ("LENGTH_LONG is a Kotlin Long variable",
                 "Long is a Kotlin number type. LENGTH_LONG is the longer Toast duration."),
                ("They choose fitXY versus centerCrop",
                 "fitXY and centerCrop are scaleType values, not Toast durations."),
            ],
            "Toast.LENGTH_SHORT is the short duration. Toast.LENGTH_LONG is the longer one.",
            "UI concepts, Toast duration",
        ),
        single(
            "What does Intent(context, DestinationActivity::class.java) create?",
            ("An Intent that moves from the current Activity to DestinationActivity",
             "The code table says that constructor creates an Intent to move from the current Activity to another Activity."),
            [
                ("An implicit Intent that names no destination",
                 "This constructor names DestinationActivity::class.java, so the destination is identified."),
                ("A Toast with LENGTH_SHORT",
                 "A Toast is Toast.makeText. This constructor builds an Intent."),
                ("A val that cannot change",
                 "val is a Kotlin declaration. This constructor builds an Intent."),
            ],
            "That constructor creates an Intent aimed at a specific destination Activity.",
            "UI concepts, Intent constructor",
        ),
        single(
            "What is an explicit Intent?",
            ("An Intent whose destination component is named directly, such as LoginActivity to ProfileActivity",
             "The navigation table says an explicit Intent directly identifies the destination, with that Login-to-Profile example."),
            [
                ("An Intent that describes an action and lets Android choose a component",
                 "An action with no named destination is an implicit Intent."),
                ("A layout constraint between two Views",
                 "Constraints belong to ConstraintLayout. An explicit Intent names an Activity."),
                ("A when branch with no destination",
                 "when is a conditional. An explicit Intent names the destination component."),
            ],
            "An explicit Intent names the destination, such as LoginActivity opening ProfileActivity.",
            "UI concepts, explicit Intent",
        ),
        single(
            "What is an implicit Intent?",
            ("An Intent that describes an action without naming the destination, so Android can choose a component",
             "The table says an implicit Intent describes an action without directly naming the destination component."),
            [
                ("An Intent that sets ProfileActivity::class.java as the destination",
                 "Naming ProfileActivity::class.java is the explicit form used in the sample."),
                ("A call to setContentView",
                 "setContentView connects a layout. An implicit Intent describes an action."),
                ("A GONE view",
                 "GONE is visibility. An implicit Intent leaves the destination for Android to resolve."),
            ],
            "An implicit Intent describes an action and does not name the destination component.",
            "UI concepts, implicit Intent",
        ),
        single(
            "What does intent.putExtra(key, value) do?",
            ("Adds data to an Intent as a key-value pair so another Activity can receive it",
             "The table says putExtra sends data from one Activity to another as a key-value pair."),
            [
                ("Reads a String extra back out of the Intent",
                 "Reading a String extra is getStringExtra."),
                ("Shows the value in a Toast only",
                 "A Toast is a temporary message. putExtra attaches data to the Intent."),
                ("Declares the XML id",
                 "The XML id is android:id. putExtra attaches data to an Intent."),
            ],
            "putExtra adds a key-value pair to the Intent for the next Activity.",
            "UI concepts, putExtra",
        ),
        single(
            "What does intent.getStringExtra(key) do?",
            ("Retrieves a String extra that was sent with the matching key",
             "The table says getStringExtra retrieves a String extra using the matching key."),
            [
                ("Puts a new extra onto the outgoing Intent",
                 "Adding an extra is putExtra."),
                ("Converts any EditText to a String without an Intent",
                 "Reading a field directly is text.toString(). getStringExtra reads an Intent extra."),
                ("Finishes the current Activity",
                 "Ending the Activity is finish()."),
            ],
            "getStringExtra retrieves a String extra by its key.",
            "UI concepts, getStringExtra",
        ),
        single(
            "What does startActivity(intent) do?",
            ("Starts the Activity specified by the Intent",
             "The table says startActivity launches the Activity described by the Intent."),
            [
                ("Connects a layout and does not open another screen",
                 "Connecting a layout is setContentView. startActivity opens the Activity in the Intent."),
                ("Deletes the extra named username",
                 "The sample stores username with putExtra. startActivity opens the destination."),
                ("Hides a View with GONE",
                 "GONE is a visibility value. startActivity launches an Activity."),
            ],
            "startActivity(intent) opens the Activity the Intent describes.",
            "UI concepts, startActivity",
        ),
        single(
            "What does finish() do in the Login → Profile sample?",
            ("Ends the current Activity so Back does not return to Login after navigating away",
             "The table says finish() ends the current Activity and can prevent Back from returning to Login."),
            [
                ("Saves the username into the Intent",
                 "The username is added with putExtra."),
                ("Reloads activity_main",
                 "activity_main is attached with setContentView. finish() ends the Activity."),
                ("Runs onStart and stays on Login",
                 "onStart makes an Activity visible. finish() ends Login so Back does not return to it."),
            ],
            "finish() ends Login so the Back button does not return to it after opening Profile.",
            "UI concepts, finish",
        ),
        single(
            "In the Login sample, which line sends the username to Profile?",
            ("intent.putExtra(\"username\", username), after the text is read inside the login button's click listener",
             "The sample reads etUsername, builds an Intent to ProfileActivity, then putExtra(\"username\", username) before startActivity."),
            [
                ("tvUsername.text = username, inside LoginActivity",
                 "tvUsername.text is assigned in ProfileActivity, after the extra is received."),
                ("intent.getStringExtra(\"username\"), before the Intent is created",
                 "getStringExtra reads the extra on the Profile side. Login sends it with putExtra."),
                ("setContentView(R.layout.activity_main)",
                 "setContentView attaches the login layout. It does not carry the username."),
            ],
            "Login sends the username with intent.putExtra(\"username\", username) from the button's click listener.",
            "UI concepts, login send",
        ),
        single(
            "In the Profile sample, which line receives the username and shows it?",
            ("val username = intent.getStringExtra(\"username\"), then tvUsername.text = username",
             "ProfileActivity reads that extra and assigns it to the TextView."),
            [
                ("btnLogin.setOnClickListener, which builds a new Intent",
                 "The click listener is on the Login side, where the Intent is created."),
                ("android:hint on etUsername",
                 "android:hint would be placeholder text. Profile reads the extra into tvUsername."),
                ("onDestroy(), which clears the TextView",
                 "onDestroy is final cleanup. The sample displays the extra with getStringExtra and tvUsername.text."),
            ],
            "ProfileActivity reads intent.getStringExtra(\"username\") and sets tvUsername.text to that value.",
            "UI concepts, profile receive",
        ),
        single(
            "What does tvUsername.text = username do?",
            ("Changes or displays text in that TextView",
             "The code table says this assignment changes or displays text in a TextView."),
            [
                ("Declares the XML id @+id/tvUsername",
                 "The id is declared in XML with android:id. This line sets the text."),
                ("Creates the Intent",
                 "The Intent is created with the Intent constructor."),
                ("Chooses Toast.LENGTH_LONG",
                 "LENGTH_LONG is a Toast duration. This line sets TextView text."),
            ],
            "tvUsername.text = username sets the text shown in that TextView.",
            "UI concepts, set text",
        ),
    ]


SETS = [
    ("module1", "MODULE 1", "Introduction to mobile development",
     "What Android is, the founding story, platforms, the version table, and Android Studio.",
     module1),
    ("module2", "MODULE 2", "Android Studio and UI controls",
     "Project structure, the Layout Editor, and TextView, EditText, Button, and ImageView.",
     module2),
    ("module3", "MODULE 3", "Views and layouts",
     "View versus ViewGroup, the layout types, and the size, spacing, and visibility distinctions.",
     module3),
    ("module4", "MODULE 4", "Activity lifecycle",
     "The phase order and what onCreate, onStart, onResume, onPause, onStop, and onDestroy are for.",
     module4),
    ("module5", "MODULE 5", "Kotlin logic and expressions",
     "Variables, val and var, types, operators, if / else, and when.",
     module5),
    ("ui", "PATTERNS", "UI code and navigation",
     "XML versus Kotlin, findViewById, Toast, explicit and implicit Intents, and the Login to Profile flow.",
     module_ui),
]


ENGINE = r"""
    const shuffle = (arr) => [...arr].sort(() => Math.random() - 0.5);
    const same = (a, b) => a.length === b.length && a.every((x) => b.includes(x));
    let deck = [];
    let i = 0;
    let correct = 0;
    let locked = false;
    let missed = [];
    let picked = new Set();
    const panel = document.getElementById("panel");
    const prog = document.getElementById("prog");
    const count = document.getElementById("count");
    const scoreline = document.getElementById("scoreline");
    function start(pool) {
      deck = shuffle(pool.map((q) => {
        if (q.type === "match") return { ...q, items: shuffle(q.items) };
        return { ...q, options: shuffle(q.options) };
      }));
      i = 0; correct = 0; missed = []; locked = false; picked = new Set();
      render();
    }
    function render() {
      if (i >= deck.length) return results();
      const q = deck[i];
      prog.style.width = ((i / deck.length) * 100) + "%";
      count.textContent = "Question " + (i + 1) + " of " + deck.length;
      scoreline.textContent = "Score " + correct;
      locked = false; picked = new Set();
      if (q.type === "match") {
        const opts = (q.choices || []).map((c) => `<option value="${c.v}">${esc(c.l)}</option>`).join("");
        panel.innerHTML = `<p class="q">${esc(q.q)}</p>
          <p class="hint">${esc(q.hint || "Classify each item.")}</p>
          <div class="match">${q.items.map((item, idx) => `
            <div class="row">
              <span>${esc(item)}</span>
              <select data-item="${idx}">
                <option value="">Choose…</option>
                ${opts}
              </select>
            </div>`).join("")}</div>
          <div class="actions"><button class="btn" id="check" type="button">Check</button></div>
          <div class="fb" id="fb"></div>`;
        document.getElementById("check").onclick = checkMatch;
        return;
      }
      const need = q.answer.length;
      panel.innerHTML = `<p class="q">${esc(q.q)}</p>
        ${q.type === "multi" ? `<p class="hint">Select ${need}, then check.</p>` : `<p class="hint">Pick one answer.</p>`}
        <div id="opts">${q.options.map((opt) => `<button class="opt" type="button" data-v="${encodeURIComponent(opt)}">${esc(opt)}</button>`).join("")}</div>
        <div class="actions">
          ${q.type === "multi" ? `<button class="btn" id="check" type="button" disabled>Check</button>` : ""}
        </div>
        <div class="fb" id="fb"></div>`;
      panel.querySelectorAll(".opt").forEach((btn) => {
        btn.onclick = () => {
          if (locked) return;
          const v = decodeURIComponent(btn.dataset.v);
          if (q.type === "single") {
            picked = new Set([v]);
            finish(q);
          } else {
            if (picked.has(v)) picked.delete(v); else {
              if (picked.size >= need) return;
              picked.add(v);
            }
            panel.querySelectorAll(".opt").forEach((b) => {
              b.classList.toggle("sel", picked.has(decodeURIComponent(b.dataset.v)));
            });
            document.getElementById("check").disabled = picked.size !== need;
          }
        };
      });
      const check = document.getElementById("check");
      if (check) check.onclick = () => finish(q);
    }
    function checkMatch() {
      if (locked) return;
      const q = deck[i];
      const selects = [...panel.querySelectorAll("select")];
      if (selects.some((s) => !s.value)) {
        const fb = document.getElementById("fb");
        fb.className = "fb no";
        fb.textContent = "Choose a category for every row.";
        return;
      }
      locked = true;
      let ok = true;
      selects.forEach((s, idx) => {
        const item = q.items[idx];
        const good = s.value === q.map[item];
        if (!good) ok = false;
        s.classList.add(good ? "ok" : "no");
      });
      after(ok, q, q.explain || "Review the classifications.");
    }
    function finish(q) {
      if (locked) return;
      locked = true;
      const chosen = [...picked];
      const ok = same(chosen, q.answer);
      panel.querySelectorAll(".opt").forEach((b) => {
        const v = decodeURIComponent(b.dataset.v);
        b.disabled = true;
        if (q.answer.includes(v)) b.classList.add("ok");
        else if (picked.has(v)) b.classList.add("no");
      });
      after(ok, q, q.explain || ("Correct: " + q.answer.join(" · ")));
    }
    const esc = (s) => String(s).replace(/[&<>]/g, (c) => ({"&":"&amp;","<":"&lt;",">":"&gt;"}[c]));
    function reasonBlock(q) {
      if (q.type === "match") {
        const labels = {};
        (q.choices || []).forEach((c) => { labels[c.v] = c.l; });
        const lines = (q.items || []).map((item) => `<li><b>${esc(item)}</b> — ${esc(labels[q.map[item]] || q.map[item])}</li>`).join("");
        return `<p class="why-h">WHY THIS IS RIGHT</p><ul class="why">${lines}</ul><p>${esc(q.explain || "")}</p>`;
      }
      const why = q.why || {};
      const right = (q.answer || []).map((a) => `<li><b>${esc(a)}</b> — ${esc(why[a] || q.explain || "")}</li>`).join("");
      const wrong = (q.options || []).filter((o) => !(q.answer || []).includes(o)).map((o) => `<li><b>${esc(o)}</b> — ${esc(why[o] || "")}</li>`).join("");
      return `<p class="why-h">WHY THIS IS RIGHT</p><ul class="why">${right}</ul>` +
        (wrong ? `<p class="why-h">WHY THE OTHERS ARE WRONG</p><ul class="why">${wrong}</ul>` : "");
    }
    function after(ok, q, msg) {
      if (ok) correct++; else missed.push({ q: q.q, msg });
      const fb = document.getElementById("fb");
      fb.className = "fb " + (ok ? "ok" : "no");
      fb.textContent = ok ? "Correct." : "Not quite.";
      let box = document.getElementById("reasons");
      if (!box) {
        box = document.createElement("div");
        box.id = "reasons";
        fb.after(box);
      }
      box.innerHTML = reasonBlock(q);
      scoreline.textContent = "Score " + correct;
      const actions = panel.querySelector(".actions");
      const next = document.createElement("button");
      next.className = "btn";
      next.type = "button";
      next.id = "next";
      next.textContent = i + 1 === deck.length ? "See results" : "Next";
      actions.replaceChildren(next);
      next.onclick = () => { i++; render(); };
    }
    function results() {
      prog.style.width = "100%";
      count.textContent = "Round complete";
      scoreline.textContent = "";
      const pct = Math.round((correct / deck.length) * 100);
      panel.innerHTML = `
        <p class="q">You scored</p>
        <div class="score">${correct} / ${deck.length}</div>
        <p class="sub" style="margin:0">${pct}% · ${missed.length ? missed.length + " to review" : "Clean round."}</p>
        ${missed.length ? `<ul class="miss">${missed.map((m) => `<li><b>${esc(m.q)}</b><br>${esc(m.msg)}</li>`).join("")}</ul>` : ""}
        <div class="actions">
          <a class="btn ghost" href="index.html">All modules</a>
          <button class="btn" id="again" type="button">Play again (shuffle)</button>
          ${missed.length ? `<button class="btn ghost" id="missed" type="button">Replay missed only</button>` : ""}
        </div>`;
      document.getElementById("again").onclick = () => start(BANK);
      const missBtn = document.getElementById("missed");
      if (missBtn) {
        missBtn.onclick = () => {
          const ids = new Set(missed.map((m) => m.q));
          start(BANK.filter((q) => ids.has(q.q)));
        };
      }
    }
    start(BANK);
"""


def validate(questions):
    seen = set()
    for q in questions:
        if q["q"] in seen:
            raise SystemExit(f"duplicate question: {q['q']}")
        seen.add(q["q"])
        if q["type"] == "match":
            values = {c["v"] for c in q["choices"]}
            if set(q["map"]) != set(q["items"]):
                raise SystemExit(f"match map mismatch: {q['q']}")
            for item, v in q["map"].items():
                if v not in values:
                    raise SystemExit(f"bad map value {v} in {q['q']}")
            continue
        if set(q["why"]) != set(q["options"]):
            raise SystemExit(f"why keys != options: {q['q']}")
        for a in q["answer"]:
            if a not in q["options"]:
                raise SystemExit(f"answer not in options: {q['q']}")
        if q["type"] == "single" and len(q["answer"]) != 1:
            raise SystemExit(f"single needs one answer: {q['q']}")
        if q["type"] == "multi" and len(q["answer"]) < 2:
            raise SystemExit(f"multi needs 2+ answers: {q['q']}")
        if not q["explain"]:
            raise SystemExit(f"missing explain: {q['q']}")


def page(title, sub, questions, file_name):
    bank = json.dumps(questions, ensure_ascii=False).replace("<", "\\u003c")
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{title}</title>
  <link rel="stylesheet" href="../theme.css" />
  <style>
    .row {{ grid-template-columns: 1fr minmax(9.5rem, 15rem); }}
  </style>
</head>
<body>
  <div class="wrap">
    <a class="exit" href="index.html">All modules</a>
    <h1>{title}</h1>
    <p class="sub">{sub} From the ICS26011 reviewer. Questions shuffle. Every answer shows why.</p>
    <div class="bar"><i id="prog"></i></div>
    <div class="meta">
      <span id="count"></span>
      <span id="scoreline"></span>
    </div>
    <div class="card" id="panel"></div>
  </div>
  <script>
    const BANK = {bank};
{ENGINE}
  </script>
</body>
</html>
"""
    (OUT / file_name).write_text(html, encoding="utf-8")


def main():
    built = []
    cards = []
    all_q = []
    for slug, label, title, blurb, factory in SETS:
        questions = factory()
        validate(questions)
        built.append((slug, label, title, blurb, questions))
        all_q.extend(questions)
        page(title, blurb, questions, f"{slug}.html")
        cards.append(
            f"""      <a class="mod" href="{slug}.html">
        <div class="n">{label} · {len(questions)}</div>
        <h2>{title}</h2>
        <p>{blurb}</p>
      </a>"""
        )
    validate(all_q)
    page(
        "Full application development set",
        f"All {len(all_q)} questions from the six modules, in one shuffle.",
        all_q,
        "exam.html",
    )
    cards.append(
        f"""      <a class="mod" href="exam.html">
        <div class="n">FULL SET · {len(all_q)}</div>
        <h2>Every question</h2>
        <p>The whole ICS26011 reviewer in one round. Replay misses when you finish.</p>
      </a>"""
    )
    index = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Application development</title>
  <link rel="stylesheet" href="../theme.css" />
</head>
<body>
  <div class="wrap">
    <a class="exit" href="../index.html">All reviewers</a>
    <h1>Application development</h1>
    <p class="sub">ICS26011 reviewer. {len(all_q)} questions across six modules. Each answer explains the right choice and the wrong ones.</p>
    <div class="dir">
{chr(10).join(cards)}
    </div>
  </div>
</body>
</html>
"""
    (OUT / "index.html").write_text(index, encoding="utf-8")
    print(f"{len(all_q)} questions")
    for slug, label, title, blurb, questions in built:
        print(f"  {slug}: {len(questions)}")


if __name__ == "__main__":
    main()
