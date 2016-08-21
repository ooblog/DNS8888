#! /usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division,print_function,absolute_import,unicode_literals
import sys
import os
import re
os.chdir(sys.path[0])
sys.path.append("LTsv")
from LTsv_printf import *
from LTsv_file   import *
#from LTsv_time   import *
#from LTsv_calc   import *
#from LTsv_joy    import *
#from LTsv_kbd    import *
from LTsv_gui    import *

DNS8888_T,DNS8888_W,DNS8888_H,DNS8888_I="DNS8888",640,380,None
DNS8888_congigpath,DNS8888_hostspath,DNS8888_resolvpath,DNS8888_temppath="DNS8888.tsv","/etc/hosts","/etc/resolv.conf","/tmp/"
DNS8888_ltsv,DNS8888_config,DNS8888_dnslist="","",""
DNS8888_fontname,DNS8888_fontsize="kantray5x5comic",12; DNS8888_font="{0},{1}".format(DNS8888_fontname,DNS8888_fontsize)
DNS8888_txtedit,DNS8888_filer,DNS8888_player="leafpad","rox","gnomemplayershell"
DNS8888_capitle,DNS8888_capwait,DNS8888_rewrite=".*",1000," - Mozilla Firefox"
DNS8888_grepwait=5000

def DNS8888_dnsadd_kernel(window_objvoid=None,window_objptr=None):
    DNS8888_resolvlist=LTsv_loadfile(DNS8888_resolvpath)
    DNS8888_resolvlist_splits=DNS8888_resolvlist.rstrip('\n').split('\n') if len(DNS8888_resolvlist) > 0 else []
    for dns in DNS8888_dnslist.rstrip('\n').split('\n'):
        if "nameserver " in LTsv_pickdatanum(dns,1):
            DNS8888_resolvlist_splits.append(LTsv_pickdatanum(dns,1))
    DNS8888_resolvlist_splits=sorted(set(DNS8888_resolvlist_splits),key=DNS8888_resolvlist_splits.index)
    DNS8888_resolvlist="".join("{0}\n".format(dns) for dns in DNS8888_resolvlist_splits)
    LTsv_saveplain(DNS8888_resolvpath,DNS8888_resolvlist)
    DNS8888_dnsexist_kernel()

def DNS8888_dnsexist_kernel():
    DNS8888_resolvlist=LTsv_loadfile(DNS8888_resolvpath)
    DNS8888_dns_splits=DNS8888_dnslist.rstrip('\n').split('\n'); DNS8888_dns_splitslen=len(DNS8888_dns_splits)
    for dns in DNS8888_dns_splits:
       if "nameserver " in dns:
           DNS8888_dns_splitslen=DNS8888_dns_splitslen-1 if dns[dns.find("nameserver ")+len("nameserver "):] in DNS8888_resolvlist else DNS8888_dns_splitslen
    LTsv_widget_disableenable(DNS8888_button_dns,True if DNS8888_dns_splitslen > 0 else False)

def DNS8888_play_kernel(window_objvoid=None,window_objptr=None):
    if len(LTsv_widget_gettext(DNS8888_combobox_flash)) > 0:
        LTsv_subprocess("{0} {1}".format(DNS8888_player,LTsv_widget_gettext(DNS8888_combobox_flash)))
        DNS8888_dnsexist_kernel()
    return 0

def DNS8888_open_kernel(window_objvoid=None,window_objptr=None):
    if len(LTsv_widget_gettext(DNS8888_combobox_flash)) > 0:
        LTsv_nicotu_open_output=LTsv_subprocess("cp {0} /tmp/debug{1}.mp4".format(LTsv_widget_gettext(DNS8888_combobox_flash),LTsv_widget_getnumber(DNS8888_combobox_flash)))
    LTsv_nicotu_filer_output=LTsv_subprocess("{0} {1}".format(DNS8888_filer,DNS8888_temppath))
    DNS8888_dnsexist_kernel()

def DNS8888_edit_shell(editerpath,filepath):
    def DNS8888_edit_kernel(callback_void=None,callback_ptr=None):
        LTsv_subprocess("{0} {1}".format(editerpath,filepath))
        DNS8888_configload(DNS8888_congigpath)
        DNS8888_dnsexist_kernel()
    return DNS8888_edit_kernel

def DNS8888_window_getID(window_objvoid=None,window_objptr=None):
    global DNS8888_T,DNS8888_W,DNS8888_H,DNS8888_I
    if LTsv_window_title(LTsv_window_foreground()) == DNS8888_T:
        DNS8888_I="{0}".format(LTsv_window_foreground())
        LTsv_widget_settext(DNS8888_entry_capitle,"{0}:{1}".format(DNS8888_T,DNS8888_I))
        LTsv_window_after(DNS8888_window,event_b=DNS8888_window_gettitle,event_i="DNS8888_window_gettitle",event_w=DNS8888_capwait)
    else:
        LTsv_window_after(DNS8888_window,event_b=DNS8888_window_getID,event_i="DNS8888_window_getID",event_w=100)

def DNS8888_window_gettitle(window_objvoid=None,window_objptr=None):
    if LTsv_window_foreground() != DNS8888_I:
        DNS8888_gettitle=LTsv_window_title(LTsv_window_foreground())
        try:
            rewrite_research=re.search(re.compile(DNS8888_capitle),DNS8888_gettitle)
        except re.error:
            None
        else:
            if rewrite_research:
                rewrite_case_first=LTsv_readlinefirsts(DNS8888_rewrite)
                for rewrite in DNS8888_rewrite.rstrip('\n').split('\n'):
                    rewrite_first=LTsv_readlinefirsts(rewrite); rewrite_rest=LTsv_readlinerest(rewrite,rewrite_first)
                    DNS8888_gettitle=re.sub(re.compile(rewrite_first),rewrite_rest,DNS8888_gettitle)
                LTsv_widget_settext(DNS8888_entry_capitle,DNS8888_gettitle)
    LTsv_window_after(DNS8888_window,event_b=DNS8888_window_gettitle,event_i="DNS8888_window_gettitle",event_w=DNS8888_capwait)

def DNS8888_grep_kernel(window_objvoid=None,window_objptr=None):
    DNS8888_combobox_number=LTsv_widget_getnumber(DNS8888_combobox_flash)
    DNS8888_greplist=[]
    DNS8888_lsof_input="lsof -n | grep Flash"
    DNS8888_lsof_output=LTsv_subprocess(DNS8888_lsof_input,LTsv_subprocess_shell=True).rstrip('\n')
    DNS8888_lsof_splits=DNS8888_lsof_output.rstrip('\n').split('\n') if len(DNS8888_lsof_output) > 0 else []
    for LTsv_lsof in DNS8888_lsof_splits:
        DNS8888_lsproc_input="ls -l /proc/{0}/fd | grep Flash".format(LTsv_pickdatanum(LTsv_lsof,0))
        DNS8888_lsproc_output=LTsv_subprocess(DNS8888_lsproc_input,LTsv_subprocess_shell=True)
        DNS8888_lsproc_splits=DNS8888_lsproc_output.rstrip('\n').split('\n') if len(DNS8888_lsproc_output) > 0 else []
        for  LTsv_lsproc in DNS8888_lsproc_splits:
            LTsv_fdproc=LTsv_lsproc[0:LTsv_lsproc.find(" ->")].rsplit(' ')[-1]
            DNS8888_greplist.append("/proc/{0}/fd/{1}\n".format(LTsv_lsof.split('\t')[0],LTsv_fdproc))
    DNS8888_greplist=sorted(set(DNS8888_greplist),key=DNS8888_greplist.index)
    LTsv_combobox_list(DNS8888_combobox_flash,"".join(DNS8888_greplist))
    LTsv_widget_setnumber(DNS8888_combobox_flash,DNS8888_combobox_number)
    LTsv_widget_disableenable(DNS8888_button_play,True if len(LTsv_widget_gettext(DNS8888_combobox_flash)) > 0 else False)
    LTsv_window_after(DNS8888_window,event_b=DNS8888_grep_kernel,event_i="DNS8888_window_grep",event_w=DNS8888_grepwait)

def DNS8888_configload(congigfile=DNS8888_congigpath):
    global DNS8888_congigpath,DNS8888_hostspath,DNS8888_resolvpath,DNS8888_temppath
    global DNS8888_ltsv,DNS8888_config,DNS8888_dnslist
    global DNS8888_fontname,DNS8888_fontsize
    global DNS8888_txtedit,DNS8888_filer,DNS8888_player
    global DNS8888_capitle,DNS8888_capwait,DNS8888_rewrite
    global DNS8888_grepwait
    DNS8888_ltsv=LTsv_loadfile(congigfile)
    DNS8888_config=LTsv_getpage(DNS8888_ltsv,"DNS8888")
    DNS8888_fontname=LTsv_readlinerest(DNS8888_config,"fontname",DNS8888_fontname)
    DNS8888_fontsize=min(max(LTsv_intstr0x(LTsv_readlinerest(DNS8888_config,"fontsize")),5),20)
    DNS8888_font="{0},{1}".format(DNS8888_fontname,DNS8888_fontsize)
    if sys.platform.startswith("win"):
        DNS8888_txtedit=LTsv_readlinerest(DNS8888_config,"txteditW","notepad")
        DNS8888_filer=LTsv_readlinerest(DNS8888_config,"filerW","start")
        DNS8888_player=LTsv_readlinerest(DNS8888_config,"playerW","mplayer2")
        DNS8888_hostspath=LTsv_readlinerest(DNS8888_config,"hostsW",DNS8888_hostspath)
        DNS8888_temppath=LTsv_readlinerest(DNS8888_config,"tempW","C:\\Documents and Settings\\%username%\\Local Settings\\Temp")
    if sys.platform.startswith("linux"):
        DNS8888_txtedit=LTsv_readlinerest(DNS8888_config,"txteditL",DNS8888_txtedit)
        DNS8888_filer=LTsv_readlinerest(DNS8888_config,"filerL",DNS8888_filer)
        DNS8888_player=LTsv_readlinerest(DNS8888_config,"playerL",DNS8888_player)
        DNS8888_hostspath=LTsv_readlinerest(DNS8888_config,"hostsL",DNS8888_hostspath)
        DNS8888_temppath=LTsv_readlinerest(DNS8888_config,"tempL",DNS8888_temppath)
    DNS8888_resolvpath=LTsv_readlinerest(DNS8888_config,"DNSresolv",DNS8888_resolvpath)
    DNS8888_capitle=LTsv_readlinerest(DNS8888_config,"captitle",DNS8888_capitle)
    DNS8888_capwait=min(max(LTsv_intstr0x(LTsv_readlinerest(DNS8888_config,"capwait",str(DNS8888_capwait))),1000),60000)
    DNS8888_grepwait=min(max(LTsv_intstr0x(LTsv_readlinerest(DNS8888_config,"grepwait",str(DNS8888_capwait))),1000),60000)
    DNS8888_rewrite=LTsv_getpage(DNS8888_ltsv,"titlerewrite")
    DNS8888_dnslist=LTsv_getpage(DNS8888_ltsv,"DNSlist")

LTsv_GUI=LTsv_guiinit()
if len(LTsv_GUI) > 0:
    DNS8888_configload(DNS8888_congigpath)
    DNS8888_buttonsize=DNS8888_fontsize*2
    DNS8888_window=LTsv_window_new(event_b=LTsv_window_exit,widget_t="DNS8888",widget_w=DNS8888_W,widget_h=DNS8888_H)
    DNS8888_label_hosts=LTsv_label_new(DNS8888_window,widget_t="hosts「{0}」".format(DNS8888_hostspath),widget_x=0,widget_y=DNS8888_buttonsize*0,widget_w=DNS8888_W,widget_h=DNS8888_buttonsize,widget_f=DNS8888_font)
    DNS8888_button_hosts=LTsv_button_new(DNS8888_window,event_b=DNS8888_edit_shell(DNS8888_txtedit,DNS8888_hostspath),widget_t="{0} {1}".format(DNS8888_txtedit,DNS8888_hostspath),widget_x=0,widget_y=DNS8888_buttonsize*1,widget_w=DNS8888_W,widget_h=DNS8888_buttonsize,widget_f=DNS8888_font)
    DNS8888_label_dns=LTsv_label_new(DNS8888_window,widget_t="DNS「nameserver 8.8.8.8」>「{0}」".format(DNS8888_resolvpath),widget_x=0,widget_y=DNS8888_buttonsize*2,widget_w=DNS8888_W,widget_h=DNS8888_buttonsize,widget_f=DNS8888_font)
    DNS8888_button_dns=LTsv_button_new(DNS8888_window,event_b=DNS8888_dnsadd_kernel,widget_t="8.8.8.8",widget_x=DNS8888_W*0//4,widget_y=DNS8888_buttonsize*3,widget_w=DNS8888_W*1//4,widget_h=DNS8888_buttonsize,widget_f=DNS8888_font)
    DNS8888_button_resolv=LTsv_button_new(DNS8888_window,event_b=DNS8888_edit_shell(DNS8888_txtedit,DNS8888_resolvpath),widget_t="{0} {1}".format(DNS8888_txtedit,DNS8888_resolvpath),widget_x=DNS8888_W*1//4,widget_y=DNS8888_buttonsize*3,widget_w=DNS8888_W*3//4,widget_h=DNS8888_buttonsize,widget_f=DNS8888_font)
    DNS8888_button_config=LTsv_button_new(DNS8888_window,event_b=DNS8888_edit_shell(DNS8888_txtedit,DNS8888_congigpath),widget_t="{0} {1}".format(DNS8888_txtedit,DNS8888_congigpath),widget_x=0,widget_y=DNS8888_H-DNS8888_buttonsize*1,widget_w=DNS8888_W,widget_h=DNS8888_buttonsize*1,widget_f=DNS8888_font)
    DNS8888_label_flash=LTsv_label_new(DNS8888_window,widget_t="flash(「lsof -n | grep Flash」>「/tmp/debug0.mp4」",widget_x=0,widget_y=DNS8888_buttonsize*4,widget_w=DNS8888_W,widget_h=DNS8888_buttonsize,widget_f=DNS8888_font)
    DNS8888_button_open=LTsv_button_new(DNS8888_window,event_b=DNS8888_open_kernel,widget_t="{0} {1}".format(DNS8888_filer,DNS8888_temppath),widget_x=DNS8888_W*0//5,widget_y=DNS8888_buttonsize*5,widget_w=DNS8888_W*1//5,widget_h=DNS8888_buttonsize,widget_f=DNS8888_font)
    DNS8888_combobox_flash=LTsv_combobox_new(DNS8888_window,event_b=None,widget_x=DNS8888_W*1//5,widget_y=DNS8888_buttonsize*5,widget_w=DNS8888_W*2//5,widget_h=DNS8888_buttonsize,widget_f=DNS8888_font)
    DNS8888_button_play=LTsv_button_new(DNS8888_window,event_b=DNS8888_play_kernel,widget_t=DNS8888_player,widget_x=DNS8888_W*3//5,widget_y=DNS8888_buttonsize*5,widget_w=DNS8888_W*2//5,widget_h=DNS8888_buttonsize,widget_f=DNS8888_font)
    DNS8888_label_capitle=LTsv_label_new(DNS8888_window,widget_t="「{0}」".format(DNS8888_capitle),widget_x=0,widget_y=DNS8888_buttonsize*6,widget_w=DNS8888_W,widget_h=DNS8888_buttonsize,widget_f=DNS8888_font)
    DNS8888_entry_capitle=LTsv_entry_new(DNS8888_window,event_b=None,widget_t="",widget_x=0,widget_y=DNS8888_buttonsize*7,widget_w=DNS8888_W,widget_h=DNS8888_buttonsize,widget_f=DNS8888_font)
    if sys.platform.startswith("win"):
        LTsv_widget_disableenable(DNS8888_button_dns,False)
        LTsv_widget_disableenable(DNS8888_button_resolv,False)
        LTsv_widget_disableenable(DNS8888_button_open,False)
#        LTsv_widget_disableenable(DNS8888_combobox_flash,False)
        LTsv_widget_disableenable(DNS8888_button_play,False)
    LTsv_widget_showhide(DNS8888_window,True)
    DNS8888_dnsexist_kernel()
    LTsv_window_after(DNS8888_window,event_b=DNS8888_window_getID,event_i="DNS8888_window_getID",event_w=10)
    if sys.platform.startswith("linux"):
        DNS8888_grep_kernel()
    LTsv_window_main(DNS8888_window)


# Copyright (c) 2016 ooblog
# License: MIT
# https://github.com/ooblog/DNS8888/blob/master/LICENSE
