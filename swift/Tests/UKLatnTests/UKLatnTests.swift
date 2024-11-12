import Testing
@testable import UKLatn


@Test func encode_DSTU_A() async throws {
    let cyr = "Доброго вечора, ми з України!"
    let lat = try encode(cyr)
    #expect(lat == "Dobroğo večora, my z Ukraïny!")
    let t = try decode(lat)
    #expect(t == cyr)
}


@Test func encode_DSTU_B() async throws {
    let cyr = "Доброго вечора, ми з України!"
    let lat = try encode(cyr, table: UKLatnTable.DSTU_9112_B)
    #expect(lat == "Dobrogho vechora, my z Ukrajiny!")
    let t = try decode(lat, table: UKLatnTable.DSTU_9112_B)
    #expect(t == cyr)
}


@Test func encode_KMU() async throws {
    let cyr = "Доброго вечора, ми з України!"
    let lat = try encode(cyr, table: UKLatnTable.KMU_55)
    #expect(lat == "Dobroho vechora, my z Ukrainy!")
    #expect(throws: UKLatnError.self) {
        try decode(lat, table: UKLatnTable.KMU_55)
    }
}

