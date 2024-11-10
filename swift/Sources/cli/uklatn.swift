import Foundation
import UkrainianLatin


@main
struct MyApp {

    static func main() {
        var stderr = ErrorStream()

        do {
            let args = try AppArgs.parse(CommandLine.arguments)
            if args.printHelp {
                AppArgs.printHelp()
            }
            else if let file = args.file {
                try transformFile(file, direction: args.direction, table: args.table)
            }
            else if let text = args.text {
                try transformText(text, direction: args.direction, table: args.table)
            }
        }
        catch let error as AppArgs.ParseError {
            AppArgs.printError(error, to: &stderr)
        }
        catch UKLatnError.invalidTable(let table) {
            AppArgs.printError(.invalidTable("\(table)"), to: &stderr)
        }
        catch {
            print(error, to: &stderr)
        }
    }

    private static func transformText(_ text: String, direction: AppArgs.TransformDirection, table: UKLatnTable) throws {
        let value: String
        switch direction {
        case .cyr2lat:
            value = try encode(text, table: table)
        case .lat2cyr:
            value = try decode(text, table: table)
        }
        print("\(value)")
    }

    private static func transformFile(_ file: String, direction: AppArgs.TransformDirection, table: UKLatnTable) throws {
        if file == "-" {
            while let text = readLine() {
                try transformText(text, direction: direction, table: table)
            }
        }
        else {
            var encoding: String.Encoding = .utf8
            let text = try String(contentsOfFile: file, usedEncoding: &encoding)
            try transformText(text, direction: direction, table: table)
        }
    }
}


private struct AppArgs {
    var executable: String = ""
    var printHelp: Bool = false
    var text: String?
    var file: String?
    var table: UKLatnTable = .DSTU_9112_A
    var direction: TransformDirection = .cyr2lat
    
    static let _usage = "usage: uklatn [-h] [-t TABLE] [-c] [-l] [-f FILE] [text ...]"
    
    static let _help = _usage +
    """
    
    
    arguments:
      text            text to transliterate
    
    options:
      -h, --help            show this help message and exit
      -t, --table {DSTU_9112_A,DSTU_9112_B,KMU_55}
                            transliteration system (default: DSTU_9112_A)
      -l, --lat, --latin    convert to Latin script (default)
      -c, --cyr, --cyrillic convert to Cyrillic script
      -f, --file FILE       read text from file
    """
    
    enum TransformDirection {
        case cyr2lat
        case lat2cyr
    }
    
    enum ParseError: Error {
        case unknownArgument(String)
        case invalidTable(String)
        case missingTableValue
        case missingFileValue
        case missingRequiredTextOrFile
    }
    
    static func printUsage<S>(to output: inout S) where S:TextOutputStream {
        print("\(_usage)", to: &output)
    }
    
    static func printHelp() {
        print("\(_help)")
    }
    
    static func printHelp<S>(to output: inout S) where S:TextOutputStream {
        print("\(_help)", to: &output)
    }
    
    static func printError<S>(_ error: ParseError, to output: inout S) where S:TextOutputStream {
        let message: String
        switch error {
        case .unknownArgument(let arg):
            message = "unrecognized arguments: \(arg)"
        case .invalidTable(let table):
            message = "invalid table: \(table)"
        case .missingTableValue:
            message = "argument -t/--table expected table name"
        case .missingFileValue:
            message = "argument -f/--file expected file name"
        case .missingRequiredTextOrFile:
            message = "missing required arguments: text or file"
        }
        printUsage(to: &output)
        print("error: \(message)", to: &output)
    }
    
    static func parse(_ argv: [String]) throws -> AppArgs {
        var args = AppArgs()
        args.executable = argv[0]
        var state: Int = 0
        
        for iarg in 1 ..< argv.count {
            let arg = argv[iarg]
            switch state {
                
            case 0:
                if arg.first == "-" {
                    switch arg {
                    case "-h", "-help", "--help":
                        args.printHelp = true
                        return args
                    case "-c", "--cyr", "--cyrillic":
                        args.direction = .lat2cyr
                    case "-l", "--lat", "--latin":
                        args.direction = .cyr2lat
                    case "-t", "--table":
                        state = 1
                    case "-f", "--file":
                        state = 2
                    default:
                        throw ParseError.unknownArgument(arg)
                    }
                }
                else if !arg.isEmpty {
                    args.text = args.text.map({ $0 + " " + arg }) ?? arg
                }
                
            case 1:
                if let table = parseTable(arg) {
                    args.table = table
                    state = 0
                }
                else {
                    throw ParseError.invalidTable(arg)
                }
                
            case 2:
                args.file = arg
                state = 0
                
            default:
                fatalError()
            }
        }
        
        switch state {
        case 1:
            throw ParseError.missingTableValue
        case 2:
            throw ParseError.missingFileValue
        default:
            break
        }
        
        if args.text == nil && args.file == nil {
            throw ParseError.missingRequiredTextOrFile
        }
        
        return args
    }
    
    private static func parseTable(_ value: String) -> UKLatnTable? {
        switch value {
        case "DSTU_9112_A": return .DSTU_9112_A
        case "DSTU_9112_B": return .DSTU_9112_B
        case "KMU_55": return .KMU_55
        default: return nil
        }
    }
}


private struct ErrorStream: TextOutputStream {
    func write(_ text: String) {
        if let data = text.data(using: .utf8) {
            FileHandle.standardError.write(data)
        }
    }
}
