// swift-tools-version:5.1

import PackageDescription

let package = Package(
    name: "uklatn",
    products: [
        .library(
            name: "UKLatn",
            targets: ["UKLatn"]),
    ],
    targets: [
        .target(
            name: "UKLatn",
            dependencies: ["_uklatn"],
            path: "swift/Sources/UKLatn"),
        .target(
            name: "_uklatn",
            path: "swift/Sources/_uklatn",
            cSettings: [
                .headerSearchPath("../../../c/include"),
            ],
            linkerSettings: [
                .linkedLibrary("icuuc"),
                .linkedLibrary("icui18n"),
            ]),
        .testTarget(
            name: "UKLatnTests",
            dependencies: ["UKLatn"],
            path: "swift/Tests/UKLatnTests"),
    ],
    swiftLanguageVersions: [.v5]
)

