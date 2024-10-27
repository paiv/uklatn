import _uklatn


public struct UKLatnTable {
    public static let DSTU_9112_A = Int(_uklatn.UklatnTable_DSTU_9112_A.rawValue)
    public static let DSTU_9112_B = Int(_uklatn.UklatnTable_DSTU_9112_B.rawValue)
    public static let KMU_55 = Int(_uklatn.UklatnTable_KMU_55.rawValue)
}


public enum UKLatnError: Error {
    case failed(code: Int)
}


public func encode(_ text: String, table: Int = 0) throws -> String {
    let n = text.utf8.count
    let dst = UnsafeMutableBufferPointer<CChar>.allocate(capacity: n * 3)
    defer {
        dst.deallocate()
    }
    let err = _uklatn.uklatn_encode(text, Int32(table), dst.baseAddress, Int32(dst.count))
    if err != 0 {
        throw UKLatnError.failed(code: Int(err))
    }
    let res = String(cString: dst.baseAddress!)
    return res
}


public func decode(_ text: String, table: Int = 0) throws -> String {
    let n = text.utf8.count
    let dst = UnsafeMutableBufferPointer<CChar>.allocate(capacity: n * 3)
    defer {
        dst.deallocate()
    }
    let err = _uklatn.uklatn_decode(text, Int32(table), dst.baseAddress, Int32(dst.count))
    if err != 0 {
        throw UKLatnError.failed(code: Int(err))
    }
    let res = String(cString: dst.baseAddress!)
    return res
}
