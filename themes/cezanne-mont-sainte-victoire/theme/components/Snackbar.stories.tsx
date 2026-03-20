import type { Meta, StoryObj } from '@storybook/react';
import Snackbar from './Snackbar';

const meta  : Meta<typeof Snackbar> = {
  title: 'Components/Snackbar',
  component: Snackbar,
  tags: ['autodocs'],
};

export default meta;
type Story = StoryObj<typeof Snackbar>;

export const Default: Story = { args={{ message: 'Item saved' }} };
export const WithAction: Story = { args={{ message: 'Item saved', action: { label: 'Undo', onClick: () => {} } }} };
