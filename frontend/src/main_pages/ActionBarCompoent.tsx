import AppBar from "@mui/material/AppBar";
import { Box, Button, Menu, MenuItem, Tooltip } from "@mui/material";
import Toolbar from "@mui/material/Toolbar";
import { useNavigate } from "react-router-dom";
import React, { useState } from "react";
import { Page, SubPage } from "../typedefs/navigation";
import { UserDataViewComponent } from "../Components/user/UserDataViewComponent";
import { useTranslation } from "react-i18next";

const pages: Page[] = [
  {
    name: "i18n_home",
    type: "button",
    link: "",
    tooltip: "i18n_home_tooltip",
  },
  {
    name: "i18n_project",
    type: "button",
    link: "project",
    tooltip: "i18n_project_tooltip",
  },
  {
    name: "i18n_train_data",
    type: "menu",
    elements: [
      {
        name: "i18n_machine_learning",
        link: "ml",
        tooltip: "i18n_machine_learning_tooltip",
      },
      {
        name: "i18n_time_series_analysis",
        link: "tsd",
        tooltip: "i18n_time_series_analysis_tooltip",
      },
    ],
    tooltip: "i18n_training_data_options",
  },
  {
    name: "i18n_data",
    type: "button",
    link: "traindata",
    tooltip: "i18n_data_tooltip",
  },
  /* {
        name: "i18n_survey",
        type: "button",
        link: "survey",
        tooltip: "i18n_survey_tooltip"
    },
    {
        name: "i18n_documentation",
        type: "menu",
        link: "documentation",
        tooltip: "i18n_documentation_tooltip"
    } */
];

/**
 * Represents a custom action bar component.
 *
 * @returns {ReactElement} The rendered action bar component.
 */
export const ActionBarComponent = () => {
  const navigate = useNavigate();

  const [menuAnchors, setMenuAnchors] = useState<any>({});
  const [activeButton, setActiveButton] = useState("");
  const { t } = useTranslation(["dialogs", "main_menu"]);

  const handleMenuToggle = (
    pageName: string,
    event: React.MouseEvent<HTMLButtonElement>,
  ) => {
    setMenuAnchors((prev: { [x: string]: any }) => ({
      ...prev,
      [pageName]: prev[pageName] ? null : event.currentTarget,
    }));
  };

  const handleMenuClose = () => {
    setMenuAnchors({});
  };

  const handleLoginSignupClick = () => {
    sessionStorage.getItem("jwt") !== "None"
      ? sessionStorage.setItem("jwt", "None")
      : navigate("/login");
  };

  const handleNavigate = (link: string, parentElement?: string) => {
    setActiveButton(parentElement ? parentElement : link);
    setMenuAnchors({});
    navigate("/" + link);
  };

  const createMenuItem = (page: any) => {
    const isActive = activeButton === page.name || activeButton === page.link;
    if (page.type === "menu" && page.elements) {
      return (
        <div key={page.name}>
          <Button
            onClick={(event) => handleMenuToggle(page.name, event)}
            sx={{
              my: 2,
              color: isActive ? "#edef00" : "white",
              display: "block",
            }}
          >
            {t(page.name, { ns: ["main_menu"] })}
          </Button>
          <Menu
            id={`menu-${page.name}`}
            anchorEl={menuAnchors[page.name]}
            open={Boolean(menuAnchors[page.name])}
            onClose={handleMenuClose}
          >
            {page.elements.map((element: SubPage) => {
              return (
                <Tooltip
                  title={t(element.tooltip, { ns: ["main_menu"] })}
                  key={element.name}
                >
                  <MenuItem
                    onClick={() => handleNavigate(element.link, page.name)}
                  >
                    {t(element.name, { ns: ["main_menu"] })}
                  </MenuItem>
                </Tooltip>
              );
            })}
          </Menu>
        </div>
      );
    } else {
      return (
        <Tooltip key={page.name} title={t(page.tooltip, { ns: ["main_menu"] })}>
          <Button
            onClick={() => handleNavigate(page.link)}
            sx={{
              my: 2,
              color: isActive ? "#edef00" : "white",
              display: "block",
            }}
          >
            {t(page.name, { ns: ["main_menu"] })}
          </Button>
        </Tooltip>
      );
    }
  };

  return (
    <AppBar
      position="fixed"
      sx={{ zIndex: (theme) => theme.zIndex.drawer + 1 }}
    >
      <Toolbar>
        <Box sx={{ flexGrow: 1, display: "flex" }}>
          {pages.map(createMenuItem)}
        </Box>
        {sessionStorage.getItem("jwt") === "None" ? (
          <Button
            color="error"
            variant="contained"
            onClick={handleLoginSignupClick}
          >
            {t("button_label.login", { ns: ["dialogs"] })}
          </Button>
        ) : (
          <UserDataViewComponent />
        )}
      </Toolbar>
    </AppBar>
  );
};
