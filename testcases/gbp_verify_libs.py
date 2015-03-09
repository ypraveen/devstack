#!/usr/bin/python

import sys
import subprocess
import logging
import os
import string
import re
import datetime
import yaml
from commands import *

# Initialize logging
logging.basicConfig(format='%(asctime)s [%(levelname)s] %(name)s - %(message)s', level=logging.WARNING)
_log = logging.getLogger( __name__ )

_log.setLevel(logging.INFO)
_log.setLevel(logging.DEBUG)

class Gbp_Verify(object):

    def __init__( self ):
      """
      Init def 
      """
      self.err_strings=['Conflict','Bad Request','Error','Unknown','Unable']
	
    def exe_command(self,command_args):
      """
      Execute system calls
      """
      proc = subprocess.Popen(command_args, shell=False,stdout=subprocess.PIPE)
      #proc.communicate()
      return proc.stdout.read()

    def gbp_action_verify(self,cmd_val,action_name,*args,**kwargs):
        """
        -- cmd_val== 0:list; 1:show
        -- action_name == UUID or name_string
        List/Show Policy Action
        kwargs addresses the need for passing required/optional params
        """
        if cmd_val == '' or action_name == '':
           _log.info('''Function Usage: gbp_action_verify 0 "abc" \n
                      --cmd_val == 0:list; 1:show\n
                       -- action_name == UUID or name_string\n''')
           return 0
        #Build the command with mandatory param 'action_name'
        if cmd_val == 0:
           cmd = 'gbp policy-action-list | grep %s'% str(action_name)
           for arg in args:
             cmd = cmd + ' | grep %s' % arg
        if cmd_val == 1:
           cmd = "gbp policy-action-show "+str(action_name)
        #_log.info(cmd)
        # Execute the policy-action-verify-cmd
        cmd_out = getoutput(cmd)
        #_log.info(cmd_out)
        # Catch for non-exception error strings, even though try clause succeded
        for err in self.err_strings:
            if re.search('\\b%s\\b' %(err), cmd_out, re.I):
               _log.info(cmd_out)
               _log.info( "Cmd execution failed! with this Return Error: \n%s" %(cmd_out))
               return 0
        if cmd_val == 0:
           for arg in args:
               if cmd_out.find(arg) == -1 or cmd_out.find(action_name) == -1:
                  _log.info(cmd_out)
                  _log.info("The Attribute== %s DID NOT MATCH for the Action == %s in LIST cmd" %(arg,action_name))
                  return 0
        # If try clause succeeds for "verify" cmd then parse the cmd_out to match the user-fed expected attributes & their values
        if cmd_val == 1:
         for arg, val in kwargs.items():
           if re.search("\\b%s\\b\s+\| \\b%s\\b.*" %(arg,val),cmd_out,re.I)==None:
             _log.info(cmd_out)
             _log.info("The Attribute== %s and its Value== %s DID NOT MATCH for the Action == %s" %(arg,val,action_name))
             return 0
        #_log.info("All attributes & values found Valid for the object Policy Action == %s" %(action_name))
	return 1     

    def gbp_classif_verify(self,cmd_val,classifier_name,*args,**kwargs):
        """
        -- cmd_val== 0:list; 1:show
        -- classifier_name == UUID or name_string
        List/Show Policy Action
        kwargs addresses the need for passing required/optional params
        """
        if cmd_val == '' or classifier_name == '':
           _log.info('''Function Usage: gbp_classif_verify(0,name) \n
                      --cmd_val == 0:list 1:show\n
                       -- classifier_name == UUID or name_string\n''')
           return 0
        #Build the command with mandatory param 'classifier_name'
        if cmd_val == 0:
           cmd = 'gbp policy-classifier-list | grep %s'% str(classifier_name)
           for arg in args:
             cmd = cmd + ' | grep %s' % arg
        if cmd_val == 1:
           cmd = "gbp policy-classifier-show "+str(classifier_name)
        # Execute the policy-classifier-verify-cmd
        cmd_out = getoutput(cmd)
        #_log.info(cmd_out)
        # Catch for non-exception error strings, even though try clause succeded
        for err in self.err_strings:
            if re.search('\\b%s\\b' %(err), cmd_out, re.I):
               _log.info(cmd_out)
               _log.info( "Cmd execution failed! with this Return Error: \n%s" %(cmd_out))
               return 0
        if cmd_val == 0:
           for arg in args:
               if cmd_out.find(arg) == -1 or cmd_out.find(classifier_name) == -1:
                  _log.info(cmd_out)
                  _log.info("The Attribute== %s DID NOT MATCH for the Classifier == %s in LIST cmd" %(arg,classifier_name))
                  return 0
        # If try clause succeeds for "verify" cmd then parse the cmd_out to match the user-fed expected attributes & their values
        if cmd_val == 1:
         for arg, val in kwargs.items():
           if re.search("\\b%s\\b\s+\| \\b%s\\b.*" %(arg,val),cmd_out,re.I)==None:
             _log.info(cmd_out)
             _log.info("The Attribute== %s and its Value== %s DID NOT MATCH for the Claasifier == %s" %(arg,val,classifier_name))
             return 0
        #_log.info("All attributes & values found Valid for the object Policy Classifier == %s" %(classifier_name))
        return 1

    def gbp_policy_verify_all(self,cmd_val,cfgobj,name_uuid,*args,**kwargs):
        """
        --cfgobj== policy-*(where *=action;classifer,rule,rule-set,target-group,target)
        --cmd_val== 0:list; 1:show
        kwargs addresses the need for passing required/optional params
        """
        cfgobj_dict={"action":"policy-action","classifier":"policy-classifier","rule":"policy-rule",
                      "ruleset":"policy-rule-set","group":"group","target":"policy-target"}
        if cfgobj != '':
           if cfgobj not in cfgobj_dict:
              raise KeyError
        if cmd_val == '' or name_uuid == '':
           _log.info('''Function Usage: gbp_policy_verify_all(0,'action','name_uuid')\n
                      --cmd_val == 0:list; 1:show\n
                      -- name_uuid == UUID or name_string\n''')
           return 0
        #Build the command with mandatory params
        if cmd_val == 0:
           cmd = 'gbp %s-list | grep ' % cfgobj_dict[cfgobj]+str(name_uuid)
           for arg in args:
             cmd = cmd + ' | grep %s' % arg
        if cmd_val == 1:
           cmd = 'gbp %s-show ' % cfgobj_dict[cfgobj]+str(name_uuid)
        # Execute the policy-object-verify-cmd
        cmd_out = getoutput(cmd)
        # Catch for non-exception error strings
        for err in self.err_strings:
            if re.search('\\b%s\\b' %(err), cmd_out, re.I):
               _log.info(cmd_out)
               _log.info( "Cmd execution failed! with this Return Error: \n%s" %(cmd_out))
               return 0
        if cmd_val == 0:
           if cmd_out == '': # The case when grep returns null
              return 0
           else :
              for arg in args:
                if cmd_out.find(arg) == -1 or cmd_out.find(name_uuid) == -1:
                  _log.info(cmd_out)
                  _log.info("The Attribute== %s DID NOT MATCH for the Policy Object == %s in LIST cmd" %(arg,cfgobj))
                  return 0
        # If "verify" cmd succeeds then parse the cmd_out to match the user-fed expected attributes & their values
        if cmd_val == 1:
         for arg, val in kwargs.items():
           if re.search("\\b%s\\b\s+\| \\b%s\\b.*" %(arg,val),cmd_out,re.I)==None:
             _log.info(cmd_out)
             _log.info("The Attribute== %s and its Value== %s DID NOT MATCH for the PolicyObject == %s" %(arg,val,cfgobj))
             return 0
        #_log.info("All attributes & values found Valid for the object Policy %s" %(cfgobj))
        return 1

    def gbp_l2l3ntk_pol_ver_all(self,cmd_val,cfgobj,name_uuid,ret='',*args,**kwargs):
        """
        --cfgobj== *policy(where *=l2;l3,network)
        --cmd_val== 0:list; 1:show
        --ret=='default' <<< function will return some attribute values depending upon the cfgobj
        kwargs addresses the need for passing required/optional params
        """
        cfgobj_dict={"l2p":"l2policy","l3p":"l3policy","nsp":"network-service-policy"}
        if cfgobj != '':
           if cfgobj not in cfgobj_dict:
              raise KeyError
        if cmd_val == '' or name_uuid == '':
           _log.info('''Function Usage: gbp_l2l3ntk_pol_ver_all(0,'l2p','name') \n
                      --cmd_val == 0:list; 1:show\n
                      --name_uuid == UUID or name_string\n''')
           return 0
        #Build the command with mandatory params
        if cmd_val == 0:
           cmd = 'gbp %s-list | grep ' % cfgobj_dict[cfgobj]+str(name_uuid)
           for arg in args:
             cmd = cmd + ' | grep %s' % arg
        if cmd_val == 1:
           cmd = 'gbp %s-show ' % cfgobj_dict[cfgobj]+str(name_uuid)
        # Execute the policy-object-verify-cmd
        cmd_out = getoutput(cmd)
        #_log.info(cmd_out)
        # Catch for non-exception error strings
        for err in self.err_strings:
            if re.search('\\b%s\\b' %(err), cmd_out, re.I):
               _log.info(cmd_out)
               _log.info( "Cmd execution failed! with this Return Error: \n%s" %(cmd_out))
               return 0
        if cmd_val == 0:
           if cmd_out == '': # The case when grep returns null
              return 0
           else :
              for arg in args:
                if cmd_out.find(arg) == -1 or cmd_out.find(name_uuid) == -1:
                  _log.info(cmd_out)
                  _log.info("The Attribute== %s DID NOT MATCH for the Policy Object == %s in LIST cmd" %(arg,cfgobj))
                  return 0
        # If "verify" succeeds cmd then parse the cmd_out to match the user-fed expected attributes & their values
        if cmd_val==1 and ret=='default':
          for arg, val in kwargs.items():
            if arg == 'network_service_params': #Had to make this extra block only for NSP
               if re.findall('(%s)' %(val),cmd_out) != []:
                  _log.info(cmd_out)
                  _log.info("The Attribute== %s and its Value== %s DID NOT MATCH for the PolicyObject == %s" %(arg,val,cfgobj))
                  return 0
            if re.search("\\b%s\\b\s+\| \\b%s\\b.*" %(arg,val),cmd_out,re.I)==None: 
              _log.info(cmd_out)
              _log.info("The Attribute== %s and its Value== %s DID NOT MATCH for the PolicyObject == %s" %(arg,val,cfgobj))
              return 0
          if cfgobj=="l2p":
             match = re.search("\\bl3_policy_id\\b\s+\| (.*) \|" ,cmd_out,re.I)
             l3pid = match.group(1)
             match  = re.search("\\bnetwork_id\\b\s+\| (.*) \|" ,cmd_out,re.I)
             ntkid = match.group(1)
             return l3pid.rstrip(),ntkid.rstrip()
          if cfgobj=="l3p":
             match = re.search("\\brouters\\b\s+\| (.*) \|" ,cmd_out,re.I)
             rtrid = match.group(1)
             return rtrid.rstrip()
        elif cmd_val == 1:
         for arg, val in kwargs.items():
           if re.search("\\b%s\\b\s+\| \\b%s\\b.*" %(arg,val),cmd_out,re.I)==None:
             _log.info(cmd_out)
             _log.info("The Attribute== %s and its Value== %s DID NOT MATCH for the PolicyObject == %s" %(arg,val,cfgobj))
             return 0
        else:
           #_log.info("All attributes & values found Valid for the Policy Object %s" %(cfgobj))
           return 1

    def neut_ver_all(self,cfgobj,name_uuid,ret='',**kwargs):
        """
        --cfgobj== net,subnet,port,router
        --ret=='default' <<< function will return some attribute values depending upon the cfgobj
        kwargs addresses the need for passing required/optional params
        """
        if name_uuid == '':
           _log.info('''Function Usage: neut_ver_all('net','name')\n
                      -- name_uuid == UUID or name_string\n''')
           return 0
        #Build the command with mandatory params
        cmd = 'neutron %s-show ' % cfgobj+str(name_uuid)
        _log.info('Neutron Cmd == %s\n' %(cmd))
        # Execute the policy-object-verify-cmd
        cmd_out = getoutput(cmd)
        _log.info(cmd_out)
        # Catch for non-exception error strings
        for err in self.err_strings:
            if re.search('\\b%s\\b' %(err), cmd_out, re.I):
               _log.info(cmd_out)
               _log.info( "Neutron Cmd execution failed! with this Return Error: \n%s" %(cmd_out))
               return 0
        if ret !='':
           match=re.search("\\b%s\\b\s+\| (.*) \|" %(ret),cmd_out,re.I)
           if match != None:
              return match.group(1).rstrip()
           else:
              return 0
        for arg, val in kwargs.items():
           if isinstance(val,list):  ## This is a case where more than 1 value is to verified for a given attribute
              for i in val:
                  if cmd_out.find(i) == -1:
                    _log.info(cmd_out)
                    _log.info("The Attribute== %s and its Value== %s DID NOT MATCH for the NeutronObject == %s" %(arg,i,cfgobj)) 
                    return 0
           else:
             if re.search("\\b%s\\b\s+\| \\b%s\\b.*" %(arg,val),cmd_out,re.I)==None:
                _log.info(cmd_out)
                _log.info("The Attribute== %s and its Value== %s DID NOT MATCH for the NeutronObject == %s" %(arg,val,cfgobj))
                return 0
        #_log.info("All attributes & values found Valid for the object Policy %s" %(cfgobj))
        return 1

    def gbp_obj_ver_attr_all_values(self,cfgobj,name_uuid,attr,values):
        """
        Function will verify multiple entries for any given attribute
        of a Policy Object
        --values=Must be a list
        """
        cfgobj_dict={"action":"policy-action","classifier":"policy-classifier","rule":"policy-rule",
                      "ruleset":"policy-rule-set","group":"group","target":"policy-target",
                      "l2p":"l2policy","l3p":"l3policy","nsp":"network-service-policy"}
        if cfgobj != '':
           if cfgobj not in cfgobj_dict:
              raise KeyError
        if not isinstance(values,list):
              raise TypeError
        #Build the command with mandatory params
        cmd = 'gbp %s-show ' % cfgobj_dict[cfgobj]+str(name_uuid)+' -F %s' %(attr)
        # Execute the policy-object-verify-cmd
        cmd_out = getoutput(cmd)
        # Catch for non-exception error strings
        for err in self.err_strings:
            if re.search('\\b%s\\b' %(err), cmd_out, re.I):
               _log.info( "Cmd execution failed! with this Return Error: \n%s" %(cmd_out))
               return 0
        _misses=[]
        for val in values:
           if cmd_out.find(val)==-1:
              _misses.append(val)
        if len(_misses)>0:
              _log.info("\nFollowing Values of the Attribute for the Policy Object was NOT FOUND=%s" %(_misses))   
              return 0
        #_log.info("All attributes & values found Valid for the object Policy %s" %(cfgobj))
        return 1

    def get_uuid_from_stack(yaml_file,heat_stack_name):
        """
        Fetches the UUID of the GBP Objects created by Heat
        """
        f = (yaml_file, 'rt')
        heat_conf = yaml.load(f)
        obj_uuid = {}
        outputs_dict = heat_conf["outputs"] # This comprise dictionary with keys as in [outputs] block of yaml-based heat template
        for key in outputs_dict.iterkeys():
            cmd = 'heat stack-show %s | grep -B 2 %s' %(heat_stack_name,key)
            cmd_out = getoutput(cmd)
            match = re.search('\"\\boutput_value\\b\": \"(.*)\"' ,cmd,re.I)
            if match != None:
               obj_uuid[key] = match.group(1)
        return obj_uuid
