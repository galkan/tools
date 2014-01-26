#!/usr/bin/ruby

require 'nmap/program'
require 'nmap/xml'
require 'tempfile'

def scan(targets, temp_file)
        targets = targets
        Nmap::Program.scan do |nmap|
                nmap.syn_scan = true
                nmap.service_scan = true
                nmap.os_fingerprint = true
                nmap.xml = temp_file
                nmap.verbose = false
                nmap.disable_dns= true
                nmap.skip_discovery = true
                nmap.syn_scan = true
                nmap.show_open_ports = true
                nmap.service_scan = false
                nmap.aggressive_timing = true
                nmap.os_fingerprint = false
                nmap.ports = [21,22,80,443,445]
                nmap.targets = targets
        end
end

def parse_nmap_reports(report_file)
        Nmap::XML.new("#{report_file}") do |xml|
                xml.each_host do |host|
                        puts "[#{host.ip}]"
                        host.each_port do |port|
                                puts "  #{port.number}/#{port.protocol}\t#{port.state}\t#{port.service}"
                        end
                end
        end
end


if __FILE__ == $0
        if ARGV.length == 1
                targets = ARGV[0]
                temp_file = Tempfile.open('nmap_tarama_sonuc')
                temp_file_path = "#{temp_file.path}"
                scan(targets,temp_file_path)
                temp_file.rewind
                parse_nmap_reports("#{temp_file.path}")
                temp_file.close
        else
                puts "Kullanim #{ARGV[0]} <ip adres>"
                exit(1)
        end
end
