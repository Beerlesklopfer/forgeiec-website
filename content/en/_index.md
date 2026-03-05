---
title: ForgeIEC
---

{{< blocks/cover title="ForgeIEC" image_anchor="top" height="full" >}}
<a class="btn btn-lg btn-primary me-3 mb-4" href="/docs/">
  Documentation <i class="fas fa-arrow-alt-circle-right ms-2"></i>
</a>
<a class="btn btn-lg btn-secondary me-3 mb-4" href="https://github.com/Beerlesklopfer/ForgeIEC/releases">
  Download <i class="fab fa-github ms-2 "></i>
</a>
<p class="lead mt-5">Open-Source IEC 61131-3 PLC Editor & Runtime for Linux</p>
{{< /blocks/cover >}}

{{% blocks/lead color="primary" %}}
ForgeIEC is a modern, open-source IEC 61131-3 PLC development environment
built with C++/Qt6 and a Rust-based gRPC runtime server.

All five IEC languages: **ST, IL, FBD, LD, SFC**
{{% /blocks/lead %}}

{{< blocks/section color="dark" type="row" >}}
{{% blocks/feature icon="fas fa-code" title="5 IEC Languages" %}}
Structured Text, Instruction List, Function Block Diagram,
Ladder Diagram, and Sequential Function Chart with tree-sitter syntax highlighting.
{{% /blocks/feature %}}

{{% blocks/feature icon="fas fa-network-wired" title="CoDeSys-style Bus System" %}}
Modbus TCP/RTU segments, device management, auto-addressing,
EtherCAT and Profibus DP bridges.
{{% /blocks/feature %}}

{{% blocks/feature icon="fas fa-bolt" title="IceOryx2 Zero-Copy IPC" %}}
PUBLISH/SUBSCRIBE keywords for zero-copy inter-process communication
between PLC programs and external systems.
{{% /blocks/feature %}}
{{< /blocks/section >}}
