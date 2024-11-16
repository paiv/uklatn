Gem::Specification.new do |s|
    s.name = 'uklatn'
    s.version = '1.13.0'
    s.license = 'MIT'
    s.summary = 'Ukrainian Cyrillic transliteration to Latin script'
    s.description = <<~EOS
    Ukraine national transliteration schemes:
    - DSTU 9112:2021,
    - KMU 55:2010 (not reversible)
    EOS
    s.author = 'Pavlo Ivashkov'
    s.homepage = 'https://github.com/paiv/uklatn'
    s.metadata = { 'source_code_uri' => 'https://github.com/paiv/uklatn' }
    s.required_ruby_version = '>= 2.6.0'
    s.files = ['ruby/lib/uklatn.rb']
end
