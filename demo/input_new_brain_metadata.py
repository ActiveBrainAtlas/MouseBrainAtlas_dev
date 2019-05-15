import sys, os

def prompt_for_choice( prompt_message, reprompt_message, list_of_choices):
    answer = None
    while answer not in list_of_choices:
        answer = raw_input( prompt_message ).lower()

        if answer in list_of_choices:
            break
        else:
            print('Please choose a response from the given options.')
            #print("Please choose an answer from the following list:")
            #print(list_of_choices)
    return answer

def prompt_and_confirm( prompt_message ):
    inputted = False
    confirmed = False
    while (not inputted) or (not confirmed):
        answer = raw_input( prompt_message )
        
        if len(answer)>0:
            inputted = True
            answer_confirmation = prompt_for_choice( "You entered \""+answer+"\", is this correct? (yes/no) : ", '', ['yes','no'] )
            
            if answer_confirmation == 'yes':
                confirmed = True
            elif answer_confirmation == 'no':
                confirmed = False
    return answer

# Prompt for Stack name
print('\n********** Stack Name **********')
stack_name = prompt_and_confirm( "Please enter the name of the stack: " )

# Prompt for cutting plane
print('\n********** Cutting Plane **********')
plane_choices = ['sagittal', 'horozontal', 'coronal']
plane = prompt_for_choice( "Please enter the cutting plane (sagittal/horozontal/coronal) : ",  '', plane_choices)

# Prompt for planar resolution
print('\n********** Planar Resolution [um] **********')
resolution_choices = ['0.46', '0.325']
resolution = prompt_for_choice( "Please enter the resolution in microns (0.46/0.325) : ",  '', resolution_choices)

# Prompt for section thickness
print('\n********** Slice Thickness **********')
thickness = prompt_and_confirm( "Please enter the slice thickness in microns (likely 20): " )

# Prompt for nissl stain name
print('\n********** Stain **********')
stain_choices = ['ntb', 'thionin']
stain = prompt_for_choice( "Please enter the nissle stain used (ntb/thionin) : ", '', stain_choices)

# Prompt whether alternating or series
print('\n********** Series (1 stain) or Alternating (2 stains) **********')
yes_no_choices = ['yes', 'no']
is_series = prompt_for_choice( "Does this brain stack use a single stain in series (yes/no) : ", '', yes_no_choices)

if is_series=='no':
    # Prompt for second stain
    print('\n********** Alternating Stain #2 **********')
    stain_2 = prompt_and_confirm( "Please enter the second stain, which alternates with the "+stain+" : " )
else:
    stain_2 = ""
print('')


print('Please confirm that all of your selections are correct.')
print('Stack name:           '+stack_name)
print('Cutting plane:        '+plane)
print('Planar resolution:    '+resolution)
print('Slice thickness:      '+thickness)
print('Stain:                '+stain)
print('Alternating stain #2: '+stain_2)
print('')
answer = prompt_for_choice( "Is this information correct? (yes/no) : ", '', yes_no_choices)
if answer=='yes':
    print('\nSaving results\n')
else:
    print('\nScrapping results\n')
    sys.exit()
    
    
# Change ntb->NTB and thionin->Thionin
if stain=='ntb':
    stain='NTB'
    detector_id=799
    img_version_1 = 'NtbNormalized'
    img_version_2 = 'NtbNormalizedAdaptiveInvertedGamma'
elif stain=='thionin':
    stain='Thionin'
    detector_id=19
    img_version_1 = 'gray'
    img_version_2 = 'gray'


# Save the STACK.ini file
def save_dict_as_ini( input_dict, fp ):
    import configparser
    assert 'DEFAULT' in input_dict.keys()

    config = configparser.ConfigParser()

    for key in input_dict.keys():
        config[key] = input_dict[key]
    
    with open(fp, 'w') as configfile:
        config.write(configfile)

input_dict = {}
input_dict['DEFAULT'] = {'stack_name': stack_name, \
                         'cutting_plane': plane,\
                         'planar_resolution_um': resolution,\
                         'section_thickness_um': thickness,\
                         'stain': stain,\
                         'stain_2_if_alternating': stain_2}
fp = os.path.join( os.environ['ROOT_DIR'], 'brains_info', stack_name+'.ini' )
try:
    os.mkdir( os.path.join( os.environ['ROOT_DIR'], 'brains_info' ) )
except:
    pass
save_dict_as_ini( input_dict, fp )


# Save the brain_metadata.sh file
fp = os.path.join( os.environ['REPO_DIR'], '..', 'setup', 'set_'+stack_name+'_metadata.sh' )

data = 'export stack='+stack_name+'\n'+\
        'export stain='+stain+'\n'+\
        'export detector_id='+str(detector_id)+'\n'+\
        'export img_version_1='+img_version_1+'\n'+\
        'export img_version_2='+img_version_2+'\n'
with open( fp, 'w' ) as file:
    file.write( data )