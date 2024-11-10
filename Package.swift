// swift-tools-version: 5.8

import PackageDescription

let package = Package(
    name: "uklatn",
    products: [
        .library(
            name: "UkrainianLatin",
            targets: ["UkrainianLatin"]),
        .executable(
            name: "uklatn",
            targets: ["cli"]),
    ],
    targets: [
        .target(
            name: "UkrainianLatin",
            path: "swift/Sources/UkrainianLatin"),
        .testTarget(
            name: "UKLatnTests",
            dependencies: ["UkrainianLatin"],
            path: "swift/Tests/UkrainianLatinTests"),
        .executableTarget(
            name: "cli",
            dependencies: ["UkrainianLatin"],
            path: "swift/Sources/cli"),
    ],
    swiftLanguageVersions: [.v5]
)
