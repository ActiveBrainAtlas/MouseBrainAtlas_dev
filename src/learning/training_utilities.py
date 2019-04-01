def sample_addresses(stacks, structure):

    positive_labels = [structure]
    negative_labels = get_negative_labels(structure, 'neg_has_all_surround',
                                          margin='500um', labels_found=all_labels)

    positive_addresses_all_stacks = {}
    negative_addresses_all_stacks = {}

    for stack in stacks:

        candidate_sections = list(chain(*[grid_indices_lookup_allStacks[stack][pl].dropna(how='any').index.tolist()
                                      for pl in positive_labels]))

        n_sections = stack_section_number[stack][structure]

        if stack_stain[stack] == 'F':
            neurotrace_sections = []
            nissl_sections = []
            for sec in candidate_sections:
                if (metadata_cache['sections_to_filenames'][stack][sec].split('-')[1][0] == 'F') \
                or stack in ['CHATM2', 'CHATM3']:
                    neurotrace_sections.append(sec)
                else:
                    nissl_sections.append(sec)
            print 'neurotrace_sections', neurotrace_sections
            print 'nissl_sections', nissl_sections
            sampled_sections = np.random.choice(neurotrace_sections, min(len(neurotrace_sections), n_sections), replace=False)
        else:
            sampled_sections = np.random.choice(candidate_sections, min(len(candidate_sections), n_sections), replace=False)

        positive_addresses_all_stacks[stack] = sorted([(stack, sec, tuple(loc))
for nl in set(positive_labels) & set(grid_indices_lookup_allStacks[stack].columns)
  for sec, locs in grid_indices_lookup_allStacks[stack][nl].loc[sampled_sections].dropna().iteritems()
  for loc in locs])

        negative_addresses_all_stacks[stack] = sorted([(stack, sec, tuple(loc))
for nl in set(negative_labels) & set(grid_indices_lookup_allStacks[stack].columns)
  for sec, locs in grid_indices_lookup_allStacks[stack][nl].loc[sampled_sections].dropna().iteritems()
  for loc in locs])

    positive_addresses = sum(positive_addresses_all_stacks.values(), [])
    negative_addresses = sum(negative_addresses_all_stacks.values(), [])

    del positive_addresses_all_stacks, negative_addresses_all_stacks

    return positive_addresses, negative_addresses