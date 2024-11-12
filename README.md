# Research Journal: [Project Title]

## Overview
- **Research Focus**: Using deep learning to train an agent who can play the Agricola boardgame relative "well". Then investigate the difference in gameplay results between competitive and collaborative players.
- **Objective**: Achieve a foundation for using boardgame in business-related, system optimization course teaching.

---

## Table of Contents
1. [Research Background](#research-background)
2. [Methodology](#methodology)
3. [Weekly Logs](#weekly-logs)
4. [Findings and Insights](#findings-and-insights)
5. [Future Work](#future-work)
6. [References](#references)

---

## Research Background
Provide background information, including:
- What inspired this research?
- Key concepts or theories.
- Literature review summaries or related work.

---

## Methodology
Document your research process:
- **Approach**: Qualitative, quantitative, mixed-methods, etc.
- **Tools**: Software, frameworks, or models used.
- **Data**: Description of datasets, sources, or sample groups.

---
<!--
## Weekly Logs
Use this section to track progress regularly. For example:

### Week 1 (MM/DD/YYYY - MM/DD/YYYY)
- **Tasks Completed**:
  - Read research papers on [topic].
  - Developed initial hypotheses.
- **Challenges**:
  - Difficulty finding data related to [specific aspect].
- **Next Steps**:
  - Explore additional data sources.
  - Begin model implementation.

### Week 2 (MM/DD/YYYY - MM/DD/YYYY)
- **Tasks Completed**:
  - Collected data from [source].
  - Cleaned and preprocessed data.
- **Insights**:
  - Found correlations between [variable A] and [variable B].
- **Next Steps**:
  - Perform exploratory data analysis (EDA).

---
-->

## Findings and Insights
Summarize your key findings as you progress:
1. **Points**:
  <table>
  <tr>
    <td align="center">
      <img src="https://github.com/user-attachments/assets/7fec3d41-2cc5-4da1-b7b3-ca00a1e653e1" width="400"/><br/>
      <b>Model 6</b>
    </td>
    <td align="center">
      <img src="https://github.com/user-attachments/assets/75d4c591-117b-4e3d-8920-977ade64c0c8" width="400"/><br/>
      <b>Model 7</b>
    </td>
    <td align="center">
      <img src="https://github.com/user-attachments/assets/041e41c8-dafd-4be6-90a0-c54e00950cec" width="400"/><br/>
      <b>Model 8</b>
    </td>
    <td align="center">
      <img src="https://github.com/user-attachments/assets/26774c62-e553-431a-9599-98260a201ba8" width="400"/><br/>
      <b>Model 9</b>
    </td>
    <td align="center">
      <img src="https://github.com/user-attachments/assets/8abe3c3e-44ba-45ac-b97c-1cfcb474f91d" width="400"/><br/>
      <b>Model 10</b>
    </td>
  </tr>
</table>
  - Compared to other training model, model 7 shows the agent had fairly low points and was gradually outperformed by partners. The reason is the agent was set to explore new strategy (entropy = 5.467057108921686e-01) while the partners stayed strict to exploitation of learned ones (entropy = 5.467057108921686e-05). Even though the result seems disappointing, it might be a good way to improve the agent's ability once it learned to beat old tricks. Though this could take more time to train. 

<!-- Add an empty line here -->

2. **Sheeps**:
  <table>
  <tr>
    <td align="center">
      <img src="https://github.com/user-attachments/assets/20f9ada0-6b7e-4b95-98f1-341176f485bb" width="400"/><br/>
      <b>Model 6</b>
    </td>
    <td align="center">
      <img src="https://github.com/user-attachments/assets/a40ce3f6-8960-482a-b37a-7cfea27b8ca4" width="400"/><br/>
      <b>Model 7</b>
    </td>
    <td align="center">
      <img src="https://github.com/user-attachments/assets/04465552-cecf-4395-8a53-6dbf39427824" width="400"/><br/>
      <b>Model 8</b>
    </td>
    <td align="center">
      <img src="https://github.com/user-attachments/assets/9baa15b4-db77-4e41-8e7a-c7b95fbe8918" width="400"/><br/>
      <b>Model 9</b>
    </td>
    <td align="center">
      <img src="https://github.com/user-attachments/assets/639a13b0-4c7c-415c-b38a-78345e7a8e09" width="400"/><br/>
      <b>Model 10</b>
    </td>
  </tr>
</table>
  - The partners seemed to be more successful than the agent in gathering sheeps. Although the agent always started strong on this (by staying strict to the learned strategies), the partners with higher entropy may have found the way to improve. In the model 8, the agent seemed to fall behind, while in model 10, with more layers of policy and value network (3x3 compared to 2x2 of previous models), the agent realized how competitive the partners are and tried to catch up. This may imply that having more layers will give the agent more flexibility and training.

<!-- Add an empty line here -->

3. **Pasteur 2**:
  <table>
  <tr>
    <td align="center">
      <img src="https://github.com/user-attachments/assets/81af07f8-cb17-40fa-895a-81bdbf0e6e77" width="400"/><br/>
      <b>Model 6</b>
    </td>
    <td align="center">
      <img src="https://github.com/user-attachments/assets/d2ae1123-5e79-4fa2-bd10-e22e2b6d889d" width="400"/><br/>
      <b>Model 7</b>
    </td>
    <td align="center">
      <img src="https://github.com/user-attachments/assets/21b7d9a6-7bdf-4340-9546-c0447b07aa45" width="400"/><br/>
      <b>Model 8</b>
    </td>
    <td align="center">
      <img src="https://github.com/user-attachments/assets/07c16410-3f44-49d3-8120-efe37cf098c8" width="400"/><br/>
      <b>Model 9</b>
    </td>
    <td align="center">
      <img src="https://github.com/user-attachments/assets/1b52bbdd-1c27-4281-ae2b-7b51bd86bc89" width="400"/><br/>
      <b>Model 10</b>
    </td>
  </tr>
</table>
  - This aligns with the result of the surge of sheeps in model 8 and 10. The partners went hard on pasteurs 2 to store the cattle. This means the partners are now capable of making level 3 moves where they need to have enough woods to by enough pasteurs to store more animals.

---

## Future Work
- Outline areas for further exploration.
- Describe ongoing experiments or steps to refine your research.

---

## References
- List citations, tools, or resources used in your research.
  - Author(s), Title, Year, DOI/Link, etc.

---

### Tips for Maintaining Your Research Journal in README.md
1. **Use Markdown Features**:
   - Headers (`#`, `##`, `###`) to organize content.
   - Bullet points (`-`, `*`) for tasks and lists.
   - Tables for structured data.
   - Hyperlinks for external references.

2. **Update Regularly**:
   - Commit updates to your README as often as necessary, ideally weekly or after completing major milestones.

3. **Version Control**:
   - Use Git's version history to track changes to your research log over time.

4. **Include Visuals**:
   - Add graphs, charts, or images to illustrate findings using Markdown syntax:
     ```markdown
     ![Description](path/to/image.png)
     ```

By keeping a well-structured README, you create a professional, transparent, and organized record of your research journey. It can also be easily shared with collaborators or used as part of your portfolio!
